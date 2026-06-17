import asyncio
from helpers.tool import Tool, Response

class MaintenanceScheduler(Tool):
    async def execute(self, equipment="", hours_run=0, maintenance_type="preventive", **kwargs):
        intervals = {
            "cnc_machine": {"preventive": 500, "predictive": 200, "overhaul": 4000},
            "hydraulic_press": {"preventive": 250, "predictive": 100, "overhaul": 2000},
            "conveyor": {"preventive": 1000, "predictive": 500, "overhaul": 8000},
            "robot": {"preventive": 2000, "predictive": 1000, "overhaul": 12000},
            "compressor": {"preventive": 500, "predictive": 250, "overhaul": 4000},
        }
        eq = equipment.lower().replace(" ", "_")
        if eq not in intervals:
            return Response(message=f"Unknown equipment: {equipment}. Known: {', '.join(intervals.keys())}", break_loop=False)
        interval = intervals[eq].get(maintenance_type, 500)
        hours_remaining = interval - (hours_run % interval)
        status = "OVERDUE" if hours_remaining <= 0 else f"{hours_remaining:.0f} hours remaining"
        return Response(message=f"{equipment} ({maintenance_type}): {status}. Interval: every {interval} hrs", break_loop=False)
