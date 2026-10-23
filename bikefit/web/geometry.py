"""Frame geometry presets for popular road bikes (model years 2025/2026).

There are no public sales figures per model, so the list combines the market
leaders in Germany with the bikes of the TOUR / RennRad bestseller tests.
Values per size: stack mm, reach mm, seat tube angle °, stock crank mm
(None where the source does not state it). Source: bikeinsights.com
geometry pages, looked up 2026-10-23. Manufacturers change details between
model years, so the UI asks the rider to compare with the geometry table.
"""

# (size, stack, reach, seat angle, crank)
_ENDURACE_2025 = [
    ("3XS", 510, 350, 73.5, 165), ("2XS", 529, 354, 73.5, 165), ("XS", 548, 370, 73.5, 170),
    ("S", 568, 375, 73.5, 170), ("M", 590, 378, 73.5, 172.5), ("L", 611, 387, 73.5, 172.5),
    ("XL", 637, 405, 73.5, 175), ("2XL", 656, 415, 73.5, 175),
]
_ULTIMATE = [
    ("2XS", 498, 372, 73.5, 165), ("XS", 520, 378, 73.5, 170), ("S", 539, 390, 73.5, 170),
    ("M", 560, 393, 73.5, 172.5), ("L", 580, 401, 73.5, 172.5), ("XL", 606, 419, 73.5, 175),
    ("2XL", 624, 429, 73.5, 175),
]

PRESETS = [
    {"marke": "Canyon", "modell": "Endurace CF SLX", "jahre": "2024–2025", "groessen": _ENDURACE_2025},
    {"marke": "Canyon", "modell": "Endurace CF SLX", "jahre": "ab 2026", "groessen": [
        ("2XS", 499, 375, 72.5, 165), ("XS", 523, 381, 73.5, 170), ("S", 542, 390, 73.5, 170),
        ("M", 563, 393, 73.5, 172.5), ("L", 583, 401, 73.5, 172.5), ("XL", 609, 419, 73.5, 175)]},
    {"marke": "Canyon", "modell": "Endurace CF", "jahre": "2024–2025", "groessen": _ENDURACE_2025},
    {"marke": "Canyon", "modell": "Ultimate CF SLX", "jahre": "2025", "groessen": _ULTIMATE},
    {"marke": "Canyon", "modell": "Aeroad CF SLX", "jahre": "2025", "groessen": _ULTIMATE},
    {"marke": "Specialized", "modell": "Tarmac SL8", "jahre": "2024–2026", "groessen": [
        ("44", 501, 366, 75.5, 165), ("49", 514, 375, 75.5, 165), ("52", 527, 380, 74.0, 170),
        ("54", 544, 384, 74.0, 172.5), ("56", 565, 395, 73.5, 172.5), ("58", 591, 402, 73.5, 175),
        ("61", 612, 408, 73.0, 175)]},
    {"marke": "Specialized", "modell": "Roubaix SL8", "jahre": "2024–2026", "groessen": [
        ("44", 543, 353, 75.0, 165), ("49", 549, 363, 74.0, 165), ("52", 566, 370, 74.0, 170),
        ("54", 585, 381, 74.0, 172.5), ("56", 605, 389, 73.5, 172.5), ("58", 630, 397, 73.5, 175)]},
    {"marke": "Specialized", "modell": "Allez", "jahre": "2025", "groessen": [
        ("44", 519, 356, 75.25, 165), ("49", 536, 359, 75.25, 165), ("52", 552, 364, 73.25, 170),
        ("54", 569, 370, 73.25, 172.5), ("56", 590, 378, 73.25, 172.5), ("58", 610, 386, 73.25, 175),
        ("61", 643, 392, 73.25, 175)]},
    {"marke": "Trek", "modell": "Domane SL (Gen 4)", "jahre": "2023–2025", "groessen": [
        ("47", 527, 364, None, None), ("50", 546, 368, None, None), ("52", 561, 371, None, None),
        ("54", 575, 374, 73.7, None), ("56", 591, 377, 73.3, 170), ("58", 611, 380, None, None),
        ("60", 632, 383, None, None), ("62", 656, 386, None, None)]},
    {"marke": "Trek", "modell": "Madone SL (Gen 8)", "jahre": "2025", "groessen": [
        ("XS", 507, 370, 73.8, 165), ("S", 530, 378, 73.8, 165), ("M", 546, 384, 73.6, 170),
        ("ML", 562, 389, 73.4, 172.5), ("L", 582, 394, 73.4, 172.5), ("XL", 610, 402, 73.4, 175)]},
    {"marke": "Giant", "modell": "TCR Advanced", "jahre": "2024–2025", "groessen": [
        ("XS", 517, 376, 74.5, 170), ("S", 528, 383, 74.0, 170), ("M", 545, 388, 73.5, 172.5),
        ("ML", 562, 393, 73.0, 172.5), ("L", 581, 402, 73.0, 175), ("XL", 597, 412, 72.5, 175)]},
    {"marke": "Giant", "modell": "Defy Advanced", "jahre": "2025", "groessen": [
        ("XS", 527, 369, 74.5, 170), ("S", 541, 375, 74.0, 170), ("M", 558, 380, 73.5, 172.5),
        ("ML", 577, 384, 73.0, 172.5), ("L", 596, 393, 73.0, 175), ("XL", 615, 402, 73.0, 175)]},
    {"marke": "Cube", "modell": "Attain", "jahre": "2025", "groessen": [
        ("47", 525, 375, 74.6, 165), ("50", 538, 378, 74.6, 170), ("53", 561, 384, 74.0, 170),
        ("56", 591, 391, 73.5, 170), ("58", 610, 394, 73.0, 175), ("60", 630, 396, 72.5, 175),
        ("62", 648, 393, 72.5, 175)]},
    {"marke": "Cube", "modell": "Agree C:62", "jahre": "2025", "groessen": [
        ("47", 513, 376, 74.6, 165), ("50", 523, 378, 74.6, 170), ("53", 543, 383, 74.0, 170),
        ("56", 572, 391, 73.5, 172.5), ("58", 591, 394, 73.0, 172.5), ("60", 606, 399, 72.5, 175),
        ("62", 628, 402, 72.5, 175)]},
    {"marke": "Rose", "modell": "Xlite 06", "jahre": "2025", "groessen": [
        ("50", 508, 372, 75.5, None), ("53", 526, 382, 75.0, None), ("55", 542, 391, 74.5, None),
        ("57", 557, 398, 74.0, None), ("59", 573, 410, 74.0, None), ("62", 597, 422, 74.0, None)]},
    {"marke": "Cannondale", "modell": "SuperSix EVO", "jahre": "2023–2026", "groessen": [
        ("44", 495, 373, 74.5, 165), ("48", 508, 376, 74.0, 165), ("50", 520, 379, 74.0, 165),
        ("52", 532, 383, 74.0, 170), ("54", 545, 387, 74.0, 170), ("56", 565, 393, 73.5, 170),
        ("58", 585, 398, 73.0, 172.5), ("61", 615, 406, 72.5, 172.5)]},
    {"marke": "Cannondale", "modell": "Synapse Carbon", "jahre": "2025", "groessen": [
        ("44", 510, 366, 73.0, None), ("48", 530, 371, 73.0, None), ("51", 550, 376, 73.0, None),
        ("54", 570, 381, 73.0, None), ("56", 590, 387, 73.0, None), ("58", 610, 393, 73.0, None),
        ("61", 640, 402, 73.0, None)]},
    {"marke": "Scott", "modell": "Addict RC", "jahre": "2025", "groessen": [
        ("XXS/47", 501, 379, 74.5, 165), ("XS/49", 513, 386, 74.5, 165), ("S/52", 526, 392, 74.0, 170),
        ("M/54", 543, 395, 73.6, 172.5), ("L/56", 565, 403, 73.3, 172.5), ("XL/58", 584, 406, 72.8, 175),
        ("XXL/61", 604, 411, 72.5, 175)]},
    {"marke": "Orbea", "modell": "Orca", "jahre": "2025–2026", "groessen": [
        ("47", 506, 370, 74.5, None), ("49", 515, 375, 74.0, None), ("51", 533, 380, 73.7, None),
        ("53", 552, 385, 73.5, None), ("55", 572, 391, 73.5, None), ("57", 590, 398, 73.2, None),
        ("60", 616, 404, 73.2, None)]},
    {"marke": "Merida", "modell": "Scultura", "jahre": "2025", "groessen": [
        ("XXS", 517, 377, 74.5, None), ("XS", 529, 383, 74.0, None), ("S", 542, 390, 74.0, None),
        ("M", 557, 395, 73.5, None), ("L", 571, 400, 73.0, None), ("XL", 593, 409, 73.0, None)]},
    {"marke": "BMC", "modell": "Roadmachine 01", "jahre": "2026", "groessen": [
        ("47", 525, 370, 74.2, 170), ("51", 550, 379, 74.2, 170), ("54", 570, 383, 74.2, 172.5),
        ("56", 595, 388, 74.2, 172.5), ("58", 620, 393, 74.2, 175), ("61", 645, 398, 74.2, 175)]},
    {"marke": "Van Rysel", "modell": "NCR CF", "jahre": "2023–2025", "groessen": [
        ("XXS", 509, 364, 74.0, 165), ("XS", 515, 382, 74.0, 165), ("S", 529, 386, 73.5, 170),
        ("M", 548, 393, 73.5, 172.5), ("L", 572, 397, 73.5, 175), ("XL", 596, 403, 73.0, 175)]},
]


def presets() -> list[dict]:
    """PRESETS with each size as a dict, ready for JSON."""
    out = []
    for i, p in enumerate(PRESETS):
        sizes = [{"groesse": g, "stack_mm": s, "reach_mm": r, "sitzwinkel_grad": a, "kurbel_mm": k}
                 for g, s, r, a, k in p["groessen"]]
        out.append({"id": i, "marke": p["marke"], "modell": p["modell"], "jahre": p["jahre"], "groessen": sizes})
    return out
