"""
FastPix Video Data API Samples

This sample demonstrates how to use the FastPix Video Data API for:
- Monitoring video performance metrics
- Analyzing viewer behavior and engagement
- Managing data dimensions and filters
- Generating comprehensive analytics reports
"""

import os
from datetime import datetime, timedelta
from fastpix_python import Fastpix, models


def setup_client():
    """Initialize the FastPix client with credentials."""
    return Fastpix(
        security=models.Security(
            username=os.getenv("FASTPIX_ACCESS_TOKEN"),
            password=os.getenv("FASTPIX_SECRET_KEY"),
        ),
    )


def analyze_performance_metrics():
    """Analyze video performance metrics."""
    with setup_client() as fastpix:
        print("=== Analyzing Performance Metrics ===")
        
        # Get overall values for views in the last 7 days
        overall_metrics = fastpix.metrics.list_overall_values(
            dimension="video",
            metric="views",
            timeframe="7d"
        )
        print(f"📊 Total views (7 days): {overall_metrics.data[0].value if overall_metrics.data else 'N/A'}")
        
        # Get breakdown by device type
        device_breakdown = fastpix.metrics.list_breakdown_values(
            dimension="device_type",
            metric="views",
            timeframe="24h"
        )
        print("📱 Views by device type:")
        for item in device_breakdown.data[:5]:  # Show top 5
            print(f"   {item.dimension_value}: {item.value}")
        
        # Get timeseries data for views
        timeseries = fastpix.metrics.get_timeseries_data(
            dimension="video",
            metric="views",
            timeframe="7d",
            interval="1d"
        )
        print(f"📈 Timeseries data points: {len(timeseries.data)}")
        
        # Compare with previous period
        comparison = fastpix.metrics.list_comparison_values(
            dimension="video",
            metric="views",
            timeframe="7d"
        )
        print(f"📊 Period comparison: {comparison.data[0].comparison if comparison.data else 'N/A'}")


def analyze_viewer_behavior():
    """Analyze viewer behavior and engagement."""
    with setup_client() as fastpix:
        print("\n=== Analyzing Viewer Behavior ===")
        
        # List video views
        video_views = fastpix.views.list_video_views(
            timeframe="7d",
            limit=10
        )
        print(f"👀 Recent video views: {len(video_views.data)}")
        
        # Get details for a specific view
        if video_views.data:
            view_details = fastpix.views.get_video_view_details(
                view_id=video_views.data[0].id
            )
            print(f"📊 View details for {view_details.media_id}:")
            print(f"   Duration: {view_details.duration} seconds")
            print(f"   Completion rate: {view_details.completion_rate}%")
        
        # List top content
        top_content = fastpix.views.list_by_top_content(
            timeframe="7d",
            limit=5
        )
        print("🏆 Top performing content:")
        for i, content in enumerate(top_content.data, 1):
            print(f"   {i}. {content.media_id} - {content.views} views")
        
        # Get concurrent viewers data
        concurrent_viewers = fastpix.views.get_data_viewlist_current_views_get_timeseries_views(
            timeframe="24h"
        )
        print(f"👥 Concurrent viewers data points: {len(concurrent_viewers.data)}")
        
        # Get viewer breakdown by dimension
        viewer_breakdown = fastpix.views.get_data_viewlist_current_views_filter(
            dimension="country",
            timeframe="7d"
        )
        print("🌍 Viewers by country:")
        for item in viewer_breakdown.data[:5]:  # Show top 5
            print(f"   {item.dimension_value}: {item.value}")


def manage_data_dimensions():
    """Manage data dimensions and filters."""
    with setup_client() as fastpix:
        print("\n=== Managing Data Dimensions ===")
        
        # List available dimensions
        dimensions = fastpix.dimensions.list_dimensions()
        print("📋 Available dimensions:")
        for dimension in dimensions.data:
            print(f"   - {dimension.name}: {dimension.description}")
        
        # Get filter values for device type dimension
        device_filters = fastpix.dimensions.list_filter_values_for_dimension(
            dimension="device_type"
        )
        print(f"\n📱 Device type filter values:")
        for value in device_filters.data:
            print(f"   - {value.value}")
        
        # Get filter values for country dimension
        country_filters = fastpix.dimensions.list_filter_values_for_dimension(
            dimension="country"
        )
        print(f"\n🌍 Country filter values (top 10):")
        for value in country_filters.data[:10]:
            print(f"   - {value.value}")


def generate_analytics_report():
    """Generate a comprehensive analytics report."""
    with setup_client() as fastpix:
        print("\n=== Generating Analytics Report ===")
        
        # Get current date for report
        report_date = datetime.now().strftime("%Y-%m-%d")
        
        print(f"📊 FastPix Analytics Report - {report_date}")
        print("=" * 50)
        
        # Performance metrics
        overall_views = fastpix.metrics.list_overall_values(
            dimension="video",
            metric="views",
            timeframe="7d"
        )
        total_views = overall_views.data[0].value if overall_views.data else 0
        print(f"📈 Total Views (7 days): {total_views:,}")
        
        # Top content
        top_content = fastpix.views.list_by_top_content(
            timeframe="7d",
            limit=3
        )
        print(f"\n🏆 Top 3 Content:")
        for i, content in enumerate(top_content.data, 1):
            print(f"   {i}. Media ID: {content.media_id} - {content.views:,} views")
        
        # Device breakdown
        device_breakdown = fastpix.metrics.list_breakdown_values(
            dimension="device_type",
            metric="views",
            timeframe="7d"
        )
        print(f"\n📱 Views by Device Type:")
        for item in device_breakdown.data:
            percentage = (item.value / total_views * 100) if total_views > 0 else 0
            print(f"   {item.dimension_value}: {item.value:,} ({percentage:.1f}%)")
        
        # Geographic distribution
        geo_breakdown = fastpix.metrics.list_breakdown_values(
            dimension="country",
            metric="views",
            timeframe="7d"
        )
        print(f"\n🌍 Top Countries:")
        for item in geo_breakdown.data[:5]:
            percentage = (item.value / total_views * 100) if total_views > 0 else 0
            print(f"   {item.dimension_value}: {item.value:,} ({percentage:.1f}%)")
        
        print("\n" + "=" * 50)
        print("✅ Report generated successfully!")


def complete_analytics_workflow():
    """Complete video data analytics workflow."""
    try:
        print("🚀 Starting FastPix Video Data API Workflow\n")
        
        # Step 1: Analyze performance metrics
        analyze_performance_metrics()
        
        # Step 2: Analyze viewer behavior
        analyze_viewer_behavior()
        
        # Step 3: Manage data dimensions
        manage_data_dimensions()
        
        # Step 4: Generate comprehensive report
        generate_analytics_report()
        
        print(f"\n🎉 Analytics workflow completed successfully!")
        print(f"💡 Use these insights to optimize your video content strategy")
        
    except Exception as e:
        print(f"❌ Error in analytics workflow: {str(e)}")


if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("FASTPIX_ACCESS_TOKEN") or not os.getenv("FASTPIX_SECRET_KEY"):
        print("❌ Please set FASTPIX_ACCESS_TOKEN and FASTPIX_SECRET_KEY environment variables")
        exit(1)
    
    complete_analytics_workflow()
