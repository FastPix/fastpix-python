// Minimal shims so this repo can typecheck the validator script without requiring node_modules installs.

// ESM `import.meta.url`
interface ImportMeta {
  url: string;
}

declare module "node:fs" {
  export const readFileSync: any;
  export const writeFileSync: any;
  export const existsSync: any;
  export const mkdirSync: any;
}

declare module "node:path" {
  export const join: any;
  export const dirname: any;
}

declare module "node:url" {
  export const fileURLToPath: any;
}

declare module "node:module" {
  export const createRequire: any;
}

declare module "node:child_process" {
  export const spawnSync: any;
}

declare module "js-yaml" {
  const yaml: any;
  export default yaml;
}

declare const process: any;
declare const Buffer: any;

