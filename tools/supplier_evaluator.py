import asyncio
from helpers.tool import Tool, Response

class SupplierEvaluator(Tool):
    async def execute(self, supplier_name="", quality_score=0, delivery_score=0, cost_score=0, ppap_status="", **kwargs):
        total = (quality_score * 0.4) + (delivery_score * 0.3) + (cost_score * 0.3)
        rating = "Preferred" if total >= 90 else "Approved" if total >= 75 else "Conditional" if total >= 60 else "Disqualified"
        return Response(message=(
            f"Supplier: {supplier_name}\n"
            f"Overall Score: {total:.1f}/100\n"
            f"Quality ({quality_score}/100) × 40%: {quality_score * 0.4:.1f}\n"
            f"Delivery ({delivery_score}/100) × 30%: {delivery_score * 0.3:.1f}\n"
            f"Cost ({cost_score}/100) × 30%: {cost_score * 0.3:.1f}\n"
            f"PPAP: {ppap_status}\n"
            f"Rating: {rating}"
        ), break_loop=False)
