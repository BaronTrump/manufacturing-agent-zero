import asyncio
from helpers.tool import Tool, Response

class OeeCalculator(Tool):
    async def execute(self, available_time=0, planned_production_time=0, ideal_cycle_time=0, total_parts=0, good_parts=0, **kwargs):
        availability = (planned_production_time / available_time * 100) if available_time > 0 else 0
        performance = ((ideal_cycle_time * total_parts) / planned_production_time * 100) if planned_production_time > 0 else 0
        quality = (good_parts / total_parts * 100) if total_parts > 0 else 0
        oee = availability * performance * quality / 10000
        return Response(message=(
            f"OEE: {oee:.1f}%\n"
            f"  Availability: {availability:.1f}%\n"
            f"  Performance: {performance:.1f}%\n"
            f"  Quality: {quality:.1f}%\n\n"
            f"World-class OEE: 85%+\n"
            f"Good: {oee >= 85:.0%}  Fair: {oee >= 60:.0%}  Needs Improvement: {oee < 60:.0%}"
        ), break_loop=False)
