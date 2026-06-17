import asyncio
from helpers.tool import Tool, Response

class QualityDefectAnalyzer(Tool):
    async def execute(self, defect_type="", quantity=0, process_stage="", severity="", **kwargs):
        defects = {
            "porosity": {
                "en": "Porosity in castings — causes: gas entrapment, shrinkage, inadequate venting. Solutions: optimize gating system, reduce pouring temp, improve venting.",
                "es": "Porosidad en fundiciones — causas: atrapamiento de gas, contracción, ventilación inadecuada. Soluciones: optimizar sistema de alimentación, reducir temp. de colada.",
                "ko": "주조품의 기공 — 원인: 가스 포집, 수축, 부적절한 배기. 해결책: 게이팅 시스템 최적화, 주입 온도 감소, 배기 개선."
            },
            "crack": {
                "en": "Cracks — causes: thermal stress, material defects, improper cooling. Solutions: adjust cooling rate, preheat material, modify fillet radii.",
                "es": "Grietas — causas: estrés térmico, defectos de material, enfriamiento inadecuado. Soluciones: ajustar velocidad de enfriamiento, precalentar material.",
                "ko": "균열 — 원인: 열응력, 재료 결함, 부적절한 냉각. 해결책: 냉각 속도 조정, 재료 예열, 필렛 반경 수정."
            },
            "dimensional": {
                "en": "Dimensional variation — causes: tool wear, thermal expansion, fixture wear. Solutions: implement SPC, increase inspection frequency, replace tooling.",
                "es": "Variación dimensional — causas: desgaste de herramienta, expansión térmica, desgaste de fijación. Soluciones: implementar SPC, aumentar frecuencia de inspección.",
                "ko": "치수 변동 — 원인: 공구 마모, 열팽창, 고정구 마모. 해결책: SPC 도입, 검사 빈도 증가, 공구 교체."
            }
        }
        info = defects.get(defect_type, {})
        return Response(message=info.get("en", "Unknown defect type"), break_loop=False)
