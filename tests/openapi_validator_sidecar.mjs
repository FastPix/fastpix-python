#!/usr/bin/env node
/**
 * Long-lived OpenAPI response-validation sidecar.
 *
 * Loads ``fixed.yaml`` once, then reads JSON-Lines validation requests from
 * stdin and writes JSON-Lines results to stdout — one request, one result.
 *
 * Request shape:
 *   {"op_id": "list-media", "status": "200", "body": {...}}
 *
 * Result shape:
 *   {"op_id": "list-media", "valid": true, "errors": []}
 *   {"op_id": "list-media", "valid": false, "errors": [{"message": "...", "path": "..."}]}
 *
 * Special commands:
 *   {"command": "ping"}    -> {"pong": true}
 *   {"command": "quit"}    -> exits with code 0
 *
 * Identical validator (`openapi-response-validator`) and ref-rewrite logic as
 * `../../node-sdk/tests/validate-get-endpoints.ts` and
 * `../../node-sdk/tests/validate-non-get-lifecycle.ts`, so verdicts match the
 * Node SDK harness exactly.
 */

import { readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { createInterface } from "node:readline";
import { createRequire } from "node:module";
import yaml from "js-yaml";

const require = createRequire(import.meta.url);
const openapiResponseValidatorMod = require("openapi-response-validator");
const OpenAPIResponseValidator =
  openapiResponseValidatorMod.default || openapiResponseValidatorMod;

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const SPEC_PATH = join(__dirname, "..", "fixed.yaml");

const spec = yaml.load(readFileSync(SPEC_PATH, "utf-8"));

function convertRefsToDefinitions(node) {
  if (node == null || typeof node !== "object") return node;
  if (Array.isArray(node)) return node.map(convertRefsToDefinitions);
  const out = {};
  for (const [k, v] of Object.entries(node)) {
    if (k === "$ref" && typeof v === "string") {
      out[k] = v.replace("#/components/schemas/", "#/definitions/");
    } else {
      out[k] = convertRefsToDefinitions(v);
    }
  }
  return out;
}

const definitions = convertRefsToDefinitions(spec.components?.schemas || {});

// Build operation_id -> { responses } index once.
const validatorByOpId = new Map();
const HTTP_METHODS = ["get", "post", "put", "patch", "delete", "head", "options"];

for (const [_path, item] of Object.entries(spec.paths || {})) {
  for (const method of HTTP_METHODS) {
    const op = item?.[method];
    if (!op?.operationId) continue;
    const responses = {};
    for (const [status, def] of Object.entries(op.responses || {})) {
      const schema = def?.content?.["application/json"]?.schema;
      if (!schema) continue;
      responses[status] = {
        description: def.description || "",
        schema: convertRefsToDefinitions(schema),
      };
    }
    if (Object.keys(responses).length === 0) continue;
    validatorByOpId.set(
      op.operationId,
      new OpenAPIResponseValidator({ responses, definitions }),
    );
  }
}

process.stderr.write(
  `[sidecar] loaded ${validatorByOpId.size} operation validators from fixed.yaml\n`,
);
// Ready signal — Python waits for this before piping requests.
process.stdout.write(JSON.stringify({ ready: true, operations: validatorByOpId.size }) + "\n");

const rl = createInterface({ input: process.stdin, terminal: false });

rl.on("line", (line) => {
  const trimmed = line.trim();
  if (!trimmed) return;
  let req;
  try {
    req = JSON.parse(trimmed);
  } catch (e) {
    process.stdout.write(JSON.stringify({ error: `bad JSON: ${e.message}` }) + "\n");
    return;
  }
  if (req.command === "ping") {
    process.stdout.write(JSON.stringify({ pong: true }) + "\n");
    return;
  }
  if (req.command === "quit") {
    process.exit(0);
  }
  const { op_id, status, body } = req;
  if (!op_id || status == null) {
    process.stdout.write(
      JSON.stringify({ op_id: op_id || null, valid: null, errors: [{ message: "missing op_id or status" }] }) + "\n",
    );
    return;
  }
  const validator = validatorByOpId.get(op_id);
  if (!validator) {
    process.stdout.write(
      JSON.stringify({ op_id, valid: null, errors: [{ message: `no validator for operationId=${op_id}` }] }) + "\n",
    );
    return;
  }
  const err = validator.validateResponse(String(status), body);
  if (!err) {
    process.stdout.write(JSON.stringify({ op_id, valid: true, errors: [] }) + "\n");
    return;
  }
  process.stdout.write(
    JSON.stringify({
      op_id,
      valid: false,
      errors: (err.errors || []).map((e) => ({
        message: e.message || "(unknown)",
        path: e.path || e.dataPath || null,
        keyword: e.keyword || null,
      })),
    }) + "\n",
  );
});

rl.on("close", () => process.exit(0));
