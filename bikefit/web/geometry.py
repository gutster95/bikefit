"""Frame geometry presets for about 100 popular road bikes and model
generations from 2016 to 2026.

There are no public sales figures per model, so the list combines the market
leaders in Germany with the bikes of the TOUR / RennRad bestseller tests and
the best-known models of the last ten years.
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
    {"brand": "Canyon", "model": "Endurace CF SLX", "years": "2024–2025", "sizes": _ENDURACE_2025},
    {"brand": "Canyon", "model": "Endurace CF SLX", "years": "2026+", "sizes": [
        ("2XS", 499, 375, 72.5, 165), ("XS", 523, 381, 73.5, 170), ("S", 542, 390, 73.5, 170),
        ("M", 563, 393, 73.5, 172.5), ("L", 583, 401, 73.5, 172.5), ("XL", 609, 419, 73.5, 175)]},
    {"brand": "Canyon", "model": "Endurace CF", "years": "2024–2025", "sizes": _ENDURACE_2025},
    {"brand": "Canyon", "model": "Ultimate CF SLX", "years": "2025", "sizes": _ULTIMATE},
    {"brand": "Canyon", "model": "Aeroad CF SLX", "years": "2025", "sizes": _ULTIMATE},
    {"brand": "Specialized", "model": "Tarmac SL8", "years": "2024–2026", "sizes": [
        ("44", 501, 366, 75.5, 165), ("49", 514, 375, 75.5, 165), ("52", 527, 380, 74.0, 170),
        ("54", 544, 384, 74.0, 172.5), ("56", 565, 395, 73.5, 172.5), ("58", 591, 402, 73.5, 175),
        ("61", 612, 408, 73.0, 175)]},
    {"brand": "Specialized", "model": "Roubaix SL8", "years": "2024–2026", "sizes": [
        ("44", 543, 353, 75.0, 165), ("49", 549, 363, 74.0, 165), ("52", 566, 370, 74.0, 170),
        ("54", 585, 381, 74.0, 172.5), ("56", 605, 389, 73.5, 172.5), ("58", 630, 397, 73.5, 175)]},
    {"brand": "Specialized", "model": "Allez", "years": "2025", "sizes": [
        ("44", 519, 356, 75.25, 165), ("49", 536, 359, 75.25, 165), ("52", 552, 364, 73.25, 170),
        ("54", 569, 370, 73.25, 172.5), ("56", 590, 378, 73.25, 172.5), ("58", 610, 386, 73.25, 175),
        ("61", 643, 392, 73.25, 175)]},
    {"brand": "Trek", "model": "Domane SL (Gen 4)", "years": "2023–2025", "sizes": [
        ("47", 527, 364, None, None), ("50", 546, 368, None, None), ("52", 561, 371, None, None),
        ("54", 575, 374, 73.7, None), ("56", 591, 377, 73.3, 170), ("58", 611, 380, None, None),
        ("60", 632, 383, None, None), ("62", 656, 386, None, None)]},
    {"brand": "Trek", "model": "Madone SL (Gen 8)", "years": "2025", "sizes": [
        ("XS", 507, 370, 73.8, 165), ("S", 530, 378, 73.8, 165), ("M", 546, 384, 73.6, 170),
        ("ML", 562, 389, 73.4, 172.5), ("L", 582, 394, 73.4, 172.5), ("XL", 610, 402, 73.4, 175)]},
    {"brand": "Giant", "model": "TCR Advanced", "years": "2024–2025", "sizes": [
        ("XS", 517, 376, 74.5, 170), ("S", 528, 383, 74.0, 170), ("M", 545, 388, 73.5, 172.5),
        ("ML", 562, 393, 73.0, 172.5), ("L", 581, 402, 73.0, 175), ("XL", 597, 412, 72.5, 175)]},
    {"brand": "Giant", "model": "Defy Advanced", "years": "2025", "sizes": [
        ("XS", 527, 369, 74.5, 170), ("S", 541, 375, 74.0, 170), ("M", 558, 380, 73.5, 172.5),
        ("ML", 577, 384, 73.0, 172.5), ("L", 596, 393, 73.0, 175), ("XL", 615, 402, 73.0, 175)]},
    {"brand": "Cube", "model": "Attain", "years": "2025", "sizes": [
        ("47", 525, 375, 74.6, 165), ("50", 538, 378, 74.6, 170), ("53", 561, 384, 74.0, 170),
        ("56", 591, 391, 73.5, 170), ("58", 610, 394, 73.0, 175), ("60", 630, 396, 72.5, 175),
        ("62", 648, 393, 72.5, 175)]},
    {"brand": "Cube", "model": "Agree C:62", "years": "2025", "sizes": [
        ("47", 513, 376, 74.6, 165), ("50", 523, 378, 74.6, 170), ("53", 543, 383, 74.0, 170),
        ("56", 572, 391, 73.5, 172.5), ("58", 591, 394, 73.0, 172.5), ("60", 606, 399, 72.5, 175),
        ("62", 628, 402, 72.5, 175)]},
    {"brand": "Rose", "model": "Xlite 06", "years": "2025", "sizes": [
        ("50", 508, 372, 75.5, None), ("53", 526, 382, 75.0, None), ("55", 542, 391, 74.5, None),
        ("57", 557, 398, 74.0, None), ("59", 573, 410, 74.0, None), ("62", 597, 422, 74.0, None)]},
    {"brand": "Cannondale", "model": "SuperSix EVO", "years": "2023–2026", "sizes": [
        ("44", 495, 373, 74.5, 165), ("48", 508, 376, 74.0, 165), ("50", 520, 379, 74.0, 165),
        ("52", 532, 383, 74.0, 170), ("54", 545, 387, 74.0, 170), ("56", 565, 393, 73.5, 170),
        ("58", 585, 398, 73.0, 172.5), ("61", 615, 406, 72.5, 172.5)]},
    {"brand": "Cannondale", "model": "Synapse Carbon", "years": "2022–2025", "sizes": [
        ("44", 510, 366, 73.0, None), ("48", 530, 371, 73.0, None), ("51", 550, 376, 73.0, None),
        ("54", 570, 381, 73.0, None), ("56", 590, 387, 73.0, None), ("58", 610, 393, 73.0, None),
        ("61", 640, 402, 73.0, None)]},
    {"brand": "Scott", "model": "Addict RC", "years": "2025", "sizes": [
        ("XXS/47", 501, 379, 74.5, 165), ("XS/49", 513, 386, 74.5, 165), ("S/52", 526, 392, 74.0, 170),
        ("M/54", 543, 395, 73.6, 172.5), ("L/56", 565, 403, 73.3, 172.5), ("XL/58", 584, 406, 72.8, 175),
        ("XXL/61", 604, 411, 72.5, 175)]},
    {"brand": "Orbea", "model": "Orca", "years": "2025–2026", "sizes": [
        ("47", 506, 370, 74.5, None), ("49", 515, 375, 74.0, None), ("51", 533, 380, 73.7, None),
        ("53", 552, 385, 73.5, None), ("55", 572, 391, 73.5, None), ("57", 590, 398, 73.2, None),
        ("60", 616, 404, 73.2, None)]},
    {"brand": "Merida", "model": "Scultura", "years": "2025", "sizes": [
        ("XXS", 517, 377, 74.5, None), ("XS", 529, 383, 74.0, None), ("S", 542, 390, 74.0, None),
        ("M", 557, 395, 73.5, None), ("L", 571, 400, 73.0, None), ("XL", 593, 409, 73.0, None)]},
    {"brand": "BMC", "model": "Roadmachine 01", "years": "2026", "sizes": [
        ("47", 525, 370, 74.2, 170), ("51", 550, 379, 74.2, 170), ("54", 570, 383, 74.2, 172.5),
        ("56", 595, 388, 74.2, 172.5), ("58", 620, 393, 74.2, 175), ("61", 645, 398, 74.2, 175)]},
    {"brand": "Van Rysel", "model": "NCR CF", "years": "2023–2025", "sizes": [
        ("XXS", 509, 364, 74.0, 165), ("XS", 515, 382, 74.0, 165), ("S", 529, 386, 73.5, 170),
        ("M", 548, 393, 73.5, 172.5), ("L", 572, 397, 73.5, 175), ("XL", 596, 403, 73.0, 175)]},
]

# Earlier model generations and further popular models (2016–2026): stack and
# reach per size from geometrygeeks.bike, looked up 2026-10-23. Seat angle
# and stock crank are not listed there, so they stay empty (None).
PRESETS += [
    {"brand": "Bianchi", "model": "Infinito CV", "years": "2017–2022", "sizes": [
        ("47", 521, 370, None, None), ("50", 539, 375, None, None), ("53", 553, 376, None, None),
        ("55", 569, 381, None, None), ("57", 585, 386, None, None), ("59", 599, 392, None, None),
        ("61", 614, 392, None, None)]},
    {"brand": "Bianchi", "model": "Oltre XR4", "years": "2017–2022", "sizes": [
        ("47", 490, 377, None, None), ("50", 498, 385, None, None), ("53", 524, 385, None, None),
        ("55", 545, 390, None, None), ("57", 556, 395, None, None), ("59", 575, 398, None, None),
        ("61", 594, 398, None, None)]},
    {"brand": "Bianchi", "model": "Specialissima", "years": "2020–2023", "sizes": [
        ("47", 495, 375, None, None), ("50", 503, 383, None, None), ("53", 529, 383, None, None),
        ("55", 545, 388, None, None), ("57", 561, 393, None, None), ("59", 580, 397, None, None),
        ("61", 601, 397, None, None)]},
    {"brand": "Bianchi", "model": "Sprint", "years": "2019–2025", "sizes": [
        ("47", 497, 377, None, None), ("50", 505, 383, None, None), ("53", 529, 384, None, None),
        ("55", 545, 388, None, None), ("57", 561, 393, None, None), ("59", 580, 396, None, None),
        ("61", 599, 397, None, None)]},
    {"brand": "BMC", "model": "Roadmachine", "years": "2017–2023", "sizes": [
        ("47", 516, 374, None, None), ("51", 541, 382, None, None), ("54", 562, 386, None, None),
        ("56", 586, 390, None, None), ("58", 610, 394, None, None), ("61", 644, 398, None, None)]},
    {"brand": "BMC", "model": "Teammachine SLR01", "years": "2016–2018", "sizes": [
        ("48", 506, 370, None, None), ("51", 530, 378, None, None), ("54", 550, 387, None, None),
        ("56", 565, 392, None, None), ("58", 584, 402, None, None), ("61", 608, 410, None, None)]},
    {"brand": "BMC", "model": "Teammachine SLR01", "years": "2019–2022", "sizes": [
        ("47", 506, 367, None, None), ("51", 530, 377, None, None), ("54", 550, 386, None, None),
        ("56", 565, 392, None, None), ("58", 584, 401, None, None), ("61", 608, 409, None, None)]},
    {"brand": "Cannondale", "model": "CAAD12", "years": "2016–2019", "sizes": [
        ("48", 516, 369, None, None), ("50", 526, 375, None, None), ("52", 536, 381, None, None),
        ("54", 551, 387, None, None), ("56", 567, 393, None, None), ("58", 584, 399, None, None),
        ("60", 603, 405, None, None), ("63", 626, 411, None, None)]},
    {"brand": "Cannondale", "model": "CAAD13", "years": "2020–2025", "sizes": [
        ("44", 505, 370, None, None), ("48", 520, 374, None, None), ("51", 535, 378, None, None),
        ("54", 555, 384, None, None), ("56", 575, 389, None, None), ("58", 595, 395, None, None),
        ("60", 615, 400, None, None), ("62", 635, 406, None, None)]},
    {"brand": "Cannondale", "model": "SuperSix EVO (Gen 2)", "years": "2016–2019", "sizes": [
        ("44", 514, 362, None, None), ("48", 516, 369, None, None), ("50", 526, 375, None, None),
        ("52", 536, 381, None, None), ("54", 551, 387, None, None), ("56", 567, 393, None, None),
        ("58", 584, 399, None, None), ("60", 603, 405, None, None), ("63", 626, 411, None, None)]},
    {"brand": "Cannondale", "model": "SuperSix EVO (Gen 3)", "years": "2020–2022", "sizes": [
        ("44", 504, 370, None, None), ("48", 519, 374, None, None), ("51", 534, 378, None, None),
        ("54", 554, 384, None, None), ("56", 574, 390, None, None), ("58", 594, 395, None, None),
        ("60", 614, 400, None, None), ("62", 634, 406, None, None)]},
    {"brand": "Cannondale", "model": "Synapse Carbon", "years": "2017–2021", "sizes": [
        ("48", 528, 362, None, None), ("51", 549, 370, None, None), ("54", 570, 378, None, None),
        ("56", 590, 386, None, None), ("58", 611, 394, None, None), ("61", 631, 402, None, None)]},
    {"brand": "Canyon", "model": "Aeroad CF SLX", "years": "2016–2020", "sizes": [
        ("2XS", 494, 363, None, None), ("XS", 512, 376, None, None), ("S", 533, 391, None, None),
        ("M", 550, 397, None, None), ("L", 570, 403, None, None), ("XL", 592, 417, None, None),
        ("2XL", 612, 423, None, None)]},
    {"brand": "Canyon", "model": "Endurace AL", "years": "2021–2025", "sizes": [
        ("3XS", 510, 350, None, None), ("2XS", 529, 354, None, None), ("XS", 548, 370, None, None),
        ("S", 568, 375, None, None), ("M", 590, 378, None, None), ("L", 611, 387, None, None),
        ("XL", 637, 405, None, None), ("2XL", 656, 414, None, None)]},
    {"brand": "Canyon", "model": "Endurace CF SL / CF SLX", "years": "2016–2020", "sizes": [
        ("2XS", 510, 360, None, None), ("XS", 532, 370, None, None), ("S", 557, 376, None, None),
        ("M", 578, 382, None, None), ("L", 604, 389, None, None), ("XL", 625, 407, None, None),
        ("2XL", 644, 417, None, None)]},
    {"brand": "Canyon", "model": "Ultimate CF SL / CF SLX", "years": "2016–2020", "sizes": [
        ("2XS", 500, 368, None, None), ("XS", 522, 378, None, None), ("S", 546, 385, None, None),
        ("M", 567, 391, None, None), ("L", 592, 399, None, None), ("XL", 613, 418, None, None),
        ("2XL", 631, 428, None, None)]},
    {"brand": "Cervélo", "model": "R3", "years": "2016–2021", "sizes": [
        ("48", 505, 360, None, None), ("51", 530, 369, None, None), ("54", 555, 378, None, None),
        ("56", 580, 387, None, None), ("58", 605, 396, None, None), ("61", 630, 405, None, None)]},
    {"brand": "Cervélo", "model": "R5", "years": "2019–2024", "sizes": [
        ("48", 499, 362, None, None), ("51", 524, 371, None, None), ("54", 548, 380, None, None),
        ("56", 572, 389, None, None), ("61", 620, 408, None, None)]},
    {"brand": "Cervélo", "model": "S5", "years": "2019–2022", "sizes": [
        ("48", 496, 367, None, None), ("51", 519, 376, None, None), ("54", 542, 384, None, None),
        ("56", 565, 392, None, None), ("58", 588, 401, None, None)]},
    {"brand": "Cervélo", "model": "Soloist", "years": "2021–2025", "sizes": [
        ("48", 491, 363, None, None), ("51", 515, 374, None, None), ("54", 540, 383, None, None),
        ("56", 565, 392, None, None), ("58", 590, 401, None, None), ("61", 615, 410, None, None)]},
    {"brand": "Colnago", "model": "C64", "years": "2019–2021", "sizes": [
        ("48s", 528, 383, None, None), ("50s", 548, 383, None, None), ("52s", 565, 384, None, None),
        ("54s", 583, 385, None, None), ("56s", 591, 398, None, None)]},
    {"brand": "Colnago", "model": "V3Rs", "years": "2019–2022", "sizes": [
        ("42s", 514, 368, None, None), ("45s", 520, 375, None, None), ("48s", 525, 380, None, None),
        ("50s", 542, 382, None, None), ("52s", 560, 384, None, None), ("54s", 578, 390, None, None),
        ("56s", 586, 400, None, None), ("58s", 604, 408, None, None)]},
    {"brand": "Colnago", "model": "V4Rs", "years": "2023–2026", "sizes": [
        ("42", 510, 370, None, None), ("45.5", 522, 375, None, None), ("48.5", 539, 383, None, None),
        ("51", 557, 388, None, None), ("53", 575, 395, None, None), ("55", 593, 403, None, None),
        ("57", 612, 410, None, None)]},
    {"brand": "Cube", "model": "Attain", "years": "2020", "sizes": [
        ("50", 538, 369, None, None), ("53", 561, 376, None, None), ("56", 591, 385, None, None),
        ("58", 610, 388, None, None), ("60", 629, 392, None, None), ("62", 649, 391, None, None)]},
    {"brand": "Cube", "model": "Litening C:68X", "years": "2020–2023", "sizes": [
        ("50", 514, 389, None, None), ("52", 524, 388, None, None), ("54", 542, 389, None, None),
        ("56", 563, 398, None, None), ("58", 580, 403, None, None), ("60", 595, 405, None, None)]},
    {"brand": "Factor", "model": "O2", "years": "2017–2022", "sizes": [
        ("49", 503, 370, None, None), ("52", 523, 376, None, None), ("54", 542, 384, None, None),
        ("56", 565, 392, None, None), ("58", 587, 401, None, None)]},
    {"brand": "Factor", "model": "Ostro VAM", "years": "2021–2025", "sizes": [
        ("49", 503, 370, None, None), ("52", 523, 376, None, None), ("54", 542, 384, None, None),
        ("56", 565, 392, None, None), ("58", 587, 401, None, None)]},
    {"brand": "Felt", "model": "AR", "years": "2016–2020", "sizes": [
        ("48", 510, 367, None, None), ("51", 523, 379, None, None), ("54", 546, 383, None, None),
        ("56", 567, 392, None, None), ("58", 588, 406, None, None), ("61", 617, 417, None, None)]},
    {"brand": "Felt", "model": "FR", "years": "2016–2020", "sizes": [
        ("43", 499, 362, None, None), ("47", 512, 369, None, None), ("51", 530, 377, None, None),
        ("54", 550, 385, None, None), ("56", 572, 394, None, None), ("58", 594, 405, None, None),
        ("61", 621, 414, None, None)]},
    {"brand": "Felt", "model": "VR", "years": "2017–2021", "sizes": [
        ("47", 539, 363, None, None), ("51", 555, 369, None, None), ("54", 576, 379, None, None),
        ("56", 595, 386, None, None), ("58", 614, 392, None, None), ("61", 633, 401, None, None)]},
    {"brand": "Focus", "model": "Izalco Max", "years": "2016–2020", "sizes": [
        ("XXS", 510, 373, None, None), ("XS", 515, 378, None, None), ("S", 521, 383, None, None),
        ("M", 537, 390, None, None), ("L", 565, 398, None, None), ("XL", 583, 406, None, None),
        ("XXL", 601, 422, None, None)]},
    {"brand": "Focus", "model": "Izalco Max", "years": "2021–2026", "sizes": [
        ("XXS", 500, 370, None, None), ("XS", 513, 375, None, None), ("S", 531, 378, None, None),
        ("M", 552, 380, None, None), ("L", 571, 399, None, None), ("XL", 592, 401, None, None),
        ("XXL", 611, 420, None, None)]},
    {"brand": "Giant", "model": "Contend", "years": "2019–2024", "sizes": [
        ("S", 541, 375, None, None), ("M", 563, 378, None, None), ("ML", 577, 384, None, None),
        ("L", 596, 393, None, None), ("XL", 615, 401, None, None)]},
    {"brand": "Giant", "model": "Contend AR", "years": "2019–2024", "sizes": [
        ("XS", 539, 371, None, None), ("S", 559, 375, None, None), ("M", 574, 380, None, None),
        ("ML", 595, 383, None, None), ("L", 614, 392, None, None), ("XL", 638, 400, None, None)]},
    {"brand": "Giant", "model": "Defy Advanced", "years": "2019–2024", "sizes": [
        ("S", 546, 374, None, None), ("M", 567, 377, None, None), ("ML", 586, 381, None, None),
        ("L", 605, 390, None, None), ("XL", 624, 398, None, None)]},
    {"brand": "Giant", "model": "Propel Advanced", "years": "2018–2022", "sizes": [
        ("XS", 517, 372, None, None), ("S", 529, 378, None, None), ("M", 545, 383, None, None),
        ("ML", 562, 398, None, None), ("L", 581, 402, None, None), ("XL", 595, 412, None, None)]},
    {"brand": "Giant", "model": "Propel Advanced", "years": "2023–2026", "sizes": [
        ("S", 528, 383, None, None), ("M", 545, 388, None, None), ("ML", 562, 393, None, None),
        ("L", 581, 402, None, None)]},
    {"brand": "Giant", "model": "TCR Advanced", "years": "2016–2020", "sizes": [
        ("XS", 517, 372, None, None), ("S", 529, 378, None, None), ("M", 545, 383, None, None),
        ("ML", 567, 398, None, None), ("L", 581, 402, None, None), ("XL", 595, 412, None, None)]},
    {"brand": "Lapierre", "model": "Aircode DRS", "years": "2019–2024", "sizes": [
        ("XS", 501, 376, None, None), ("S", 516, 383, None, None), ("M", 538, 393, None, None),
        ("L", 557, 403, None, None), ("XL", 580, 415, None, None), ("XXL", 600, 428, None, None)]},
    {"brand": "Lapierre", "model": "Pulsium", "years": "2018–2022", "sizes": [
        ("XS", 525, 374, None, None), ("S", 546, 373, None, None), ("M", 564, 378, None, None),
        ("L", 583, 387, None, None), ("XL", 606, 394, None, None)]},
    {"brand": "Lapierre", "model": "Sensium", "years": "2016–2021", "sizes": [
        ("XS", 517, 377, None, None), ("S", 538, 378, None, None), ("M", 559, 376, None, None),
        ("L", 579, 382, None, None), ("XL", 600, 390, None, None), ("XXL", 618, 394, None, None)]},
    {"brand": "Lapierre", "model": "Xelius SL", "years": "2018–2023", "sizes": [
        ("XS", 501, 376, None, None), ("S", 516, 377, None, None), ("M", 538, 385, None, None),
        ("L", 557, 394, None, None), ("XL", 580, 402, None, None), ("XXL", 599, 415, None, None)]},
    {"brand": "Liv", "model": "Langma", "years": "2019–2024", "sizes": [
        ("XS", 516, 370, None, None), ("S", 532, 376, None, None), ("M", 553, 382, None, None),
        ("L", 569, 386, None, None)]},
    {"brand": "Merida", "model": "Reacto", "years": "2019–2022", "sizes": [
        ("XXS", 517, 377, None, None), ("XS", 529, 384, None, None), ("S", 542, 390, None, None),
        ("M", 557, 395, None, None), ("L", 571, 400, None, None), ("XL", 593, 409, None, None)]},
    {"brand": "Merida", "model": "Scultura (Gen 4)", "years": "2017–2021", "sizes": [
        ("XXS", 519, 376, None, None), ("XS", 529, 373, None, None), ("S", 542, 384, None, None),
        ("SM", 555, 386, None, None), ("ML", 574, 390, None, None), ("L", 593, 394, None, None),
        ("XL", 619, 401, None, None)]},
    {"brand": "Merida", "model": "Scultura Endurance", "years": "2021–2025", "sizes": [
        ("XXS", 539, 360, None, None), ("XS", 552, 366, None, None), ("S", 565, 376, None, None),
        ("M", 584, 380, None, None), ("L", 603, 389, None, None), ("XL", 629, 397, None, None)]},
    {"brand": "Orbea", "model": "Orca Aero", "years": "2021–2025", "sizes": [
        ("47", 496, 370, None, None), ("49", 505, 376, None, None), ("51", 523, 380, None, None),
        ("53", 542, 385, None, None), ("55", 562, 391, None, None), ("57", 580, 398, None, None),
        ("60", 606, 404, None, None)]},
    {"brand": "Pinarello", "model": "Dogma F", "years": "2022–2025", "sizes": [
        ("43", 502, 351, None, None), ("46.5", 518, 365, None, None), ("50", 525, 372, None, None),
        ("51.5", 532, 378, None, None), ("53", 543, 383, None, None), ("54", 551, 385, None, None),
        ("55", 562, 389, None, None), ("56", 570, 391, None, None), ("57.5", 585, 397, None, None),
        ("59.5", 613, 393, None, None), ("62", 652, 410, None, None)]},
    {"brand": "Pinarello", "model": "Dogma F12", "years": "2019–2021", "sizes": [
        ("42", 498, 349, None, None), ("44", 506, 354, None, None), ("46.5", 518, 365, None, None),
        ("50", 525, 372, None, None), ("51.5", 532, 378, None, None), ("53", 543, 383, None, None),
        ("54", 551, 385, None, None), ("55", 562, 389, None, None), ("56", 570, 391, None, None),
        ("57.5", 585, 397, None, None), ("59.5", 613, 393, None, None), ("62", 652, 410, None, None)]},
    {"brand": "Pinarello", "model": "F7 / F5", "years": "2023–2025", "sizes": [
        ("43", 502, 351, None, None), ("46.5", 518, 365, None, None), ("50", 526, 372, None, None),
        ("51.5", 532, 378, None, None), ("53", 543, 386, None, None), ("54.5", 558, 388, None, None),
        ("56", 570, 391, None, None), ("57.5", 599, 395, None, None), ("59.5", 634, 400, None, None)]},
    {"brand": "Pinarello", "model": "Paris", "years": "2021–2023", "sizes": [
        ("43", 512, 347, None, None), ("46", 524, 358, None, None), ("49", 537, 367, None, None),
        ("51.5", 549, 374, None, None), ("53", 560, 378, None, None), ("54.5", 573, 382, None, None),
        ("56", 587, 385, None, None), ("58", 605, 389, None, None), ("60", 625, 393, None, None)]},
    {"brand": "Pinarello", "model": "Prince", "years": "2020–2023", "sizes": [
        ("46", 523, 364, None, None), ("49", 532, 370, None, None), ("51.5", 543, 376, None, None),
        ("53", 554, 380, None, None), ("54.5", 570, 385, None, None), ("56", 586, 388, None, None),
        ("58", 606, 392, None, None), ("60", 642, 398, None, None)]},
    {"brand": "Radon", "model": "Vaillant", "years": "2022–2025", "sizes": [
        ("XS", 517, 374, None, None), ("S", 540, 380, None, None), ("M", 557, 388, None, None),
        ("L", 577, 396, None, None), ("XL", 599, 404, None, None)]},
    {"brand": "Ribble", "model": "Endurance AL", "years": "2019–2024", "sizes": [
        ("XS", 505, 379, None, None), ("S", 527, 385, None, None), ("M", 548, 388, None, None),
        ("L", 568, 394, None, None), ("XL", 589, 400, None, None)]},
    {"brand": "Ribble", "model": "Endurance SL R", "years": "2019–2024", "sizes": [
        ("XS", 498, 382, None, None), ("S", 521, 385, None, None), ("M", 541, 390, None, None),
        ("L", 562, 396, None, None), ("XL", 582, 402, None, None)]},
    {"brand": "Ribble", "model": "Ultra SL R", "years": "2021–2025", "sizes": [
        ("XS", 506, 379, None, None), ("S", 523, 385, None, None), ("M", 545, 392, None, None),
        ("L", 564, 401, None, None), ("XL", 583, 410, None, None)]},
    {"brand": "Ridley", "model": "Falcn RS", "years": "2024–2026", "sizes": [
        ("XXS", 492, 374, None, None), ("XS", 513, 378, None, None), ("S", 530, 388, None, None),
        ("M", 551, 397, None, None), ("L", 573, 404, None, None), ("XL", 599, 411, None, None)]},
    {"brand": "Ridley", "model": "Helium SLX", "years": "2017–2022", "sizes": [
        ("XXS", 507, 379, None, None), ("XS", 526, 374, None, None), ("S", 542, 384, None, None),
        ("M", 573, 390, None, None), ("L", 599, 396, None, None), ("XL", 625, 403, None, None)]},
    {"brand": "Ridley", "model": "Noah Fast", "years": "2018–2022", "sizes": [
        ("XS", 516, 378, None, None), ("S", 541, 385, None, None), ("M", 565, 393, None, None),
        ("L", 591, 401, None, None), ("XL", 616, 409, None, None)]},
    {"brand": "Rose", "model": "X-Lite Four", "years": "2019–2021", "sizes": [
        ("50", 520, 373, None, None), ("53", 538, 380, None, None), ("55", 555, 386, None, None),
        ("57", 572, 394, None, None), ("59", 591, 402, None, None), ("62", 611, 416, None, None)]},
    {"brand": "Scott", "model": "Addict", "years": "2016–2018", "sizes": [
        ("47", 503, 370, None, None), ("49", 509, 379, None, None), ("52", 527, 384, None, None),
        ("54", 547, 389, None, None), ("56", 568, 394, None, None), ("58", 588, 400, None, None),
        ("61", 608, 403, None, None)]},
    {"brand": "Scott", "model": "Addict (Endurance)", "years": "2020–2025", "sizes": [
        ("47", 522, 372, None, None), ("49", 534, 378, None, None), ("52", 557, 382, None, None),
        ("54", 578, 386, None, None), ("56", 599, 389, None, None), ("58", 619, 394, None, None),
        ("61", 638, 402, None, None)]},
    {"brand": "Scott", "model": "Addict RC", "years": "2019–2024", "sizes": [
        ("47", 502, 370, None, None), ("49", 509, 378, None, None), ("52", 526, 384, None, None),
        ("54", 547, 388, None, None), ("56", 568, 394, None, None), ("58", 588, 400, None, None),
        ("61", 607, 403, None, None)]},
    {"brand": "Specialized", "model": "Aethos", "years": "2021–2025", "sizes": [
        ("49", 514, 375, None, None), ("52", 527, 380, None, None), ("54", 544, 384, None, None),
        ("56", 565, 395, None, None), ("58", 591, 402, None, None), ("61", 612, 408, None, None)]},
    {"brand": "Specialized", "model": "Allez", "years": "2018–2024", "sizes": [
        ("44", 516, 365, None, None), ("49", 535, 374, None, None), ("52", 552, 376, None, None),
        ("54", 570, 380, None, None), ("56", 596, 385, None, None), ("58", 627, 390, None, None),
        ("61", 649, 396, None, None)]},
    {"brand": "Specialized", "model": "Allez Sprint", "years": "2017–2025", "sizes": [
        ("49", 496, 387, None, None), ("52", 507, 389, None, None), ("54", 527, 394, None, None),
        ("56", 547, 404, None, None), ("58", 576, 410, None, None), ("61", 597, 415, None, None)]},
    {"brand": "Specialized", "model": "Roubaix (Gen 3)", "years": "2020–2023", "sizes": [
        ("44", 540, 353, None, None), ("49", 555, 363, None, None), ("52", 570, 368, None, None),
        ("54", 585, 376, None, None), ("56", 605, 384, None, None), ("58", 630, 392, None, None),
        ("61", 665, 398, None, None), ("64", 675, 404, None, None)]},
    {"brand": "Specialized", "model": "Tarmac SL6", "years": "2017–2020", "sizes": [
        ("44", 500, 365, None, None), ("49", 514, 375, None, None), ("52", 527, 380, None, None),
        ("54", 544, 384, None, None), ("56", 565, 395, None, None), ("58", 591, 402, None, None),
        ("61", 612, 408, None, None)]},
    {"brand": "Specialized", "model": "Tarmac SL7", "years": "2021–2023", "sizes": [
        ("44", 491, 369, None, None), ("49", 504, 378, None, None), ("52", 517, 383, None, None),
        ("54", 534, 387, None, None), ("56", 555, 398, None, None), ("58", 581, 405, None, None),
        ("61", 602, 411, None, None)]},
    {"brand": "Specialized", "model": "Venge", "years": "2019–2020", "sizes": [
        ("49", 504, 378, None, None), ("52", 517, 383, None, None), ("54", 534, 387, None, None),
        ("56", 555, 398, None, None), ("58", 581, 405, None, None), ("61", 602, 411, None, None)]},
    {"brand": "Stevens", "model": "Arcalis", "years": "2016–2020", "sizes": [
        ("50", 513, 370, None, None), ("52", 524, 380, None, None), ("54", 545, 380, None, None),
        ("56", 562, 389, None, None), ("58", 587, 397, None, None), ("60", 605, 403, None, None),
        ("62", 625, 404, None, None)]},
    {"brand": "Stevens", "model": "Comet", "years": "2021–2025", "sizes": [
        ("50", 517, 379, None, None), ("52", 523, 380, None, None), ("54", 544, 382, None, None),
        ("56", 567, 387, None, None), ("58", 585, 397, None, None), ("60", 610, 404, None, None)]},
    {"brand": "Trek", "model": "Domane AL", "years": "2020–2026", "sizes": [
        ("47", 527, 364, None, None), ("50", 546, 368, None, None), ("52", 561, 371, None, None),
        ("54", 575, 374, None, None), ("56", 591, 377, None, None), ("58", 611, 380, None, None),
        ("60", 632, 383, None, None), ("62", 656, 386, None, None)]},
    {"brand": "Trek", "model": "Domane SL/SLR (Gen 3)", "years": "2017–2019", "sizes": [
        ("50", 546, 368, None, None), ("52", 561, 371, None, None), ("54", 575, 374, None, None),
        ("56", 591, 377, None, None), ("58", 611, 380, None, None), ("60", 632, 383, None, None),
        ("62", 656, 386, None, None)]},
    {"brand": "Trek", "model": "Madone SLR (Gen 6)", "years": "2019–2022", "sizes": [
        ("50", 521, 378, None, None), ("52", 533, 383, None, None), ("54", 541, 386, None, None),
        ("56", 563, 391, None, None), ("58", 581, 396, None, None), ("60", 601, 399, None, None),
        ("62", 620, 403, None, None)]},
    {"brand": "Trek", "model": "Émonda SL/SLR (Gen 6)", "years": "2021–2025", "sizes": [
        ("47", 507, 373, None, None), ("50", 521, 378, None, None), ("52", 533, 383, None, None),
        ("54", 541, 386, None, None), ("56", 563, 391, None, None), ("58", 581, 396, None, None),
        ("60", 601, 399, None, None), ("62", 620, 403, None, None)]},
    {"brand": "Van Rysel", "model": "EDR AF", "years": "2020–2023", "sizes": [
        ("XXS", 519, 361, None, None), ("XS", 520, 381, None, None), ("S", 532, 385, None, None),
        ("M", 551, 392, None, None), ("L", 575, 396, None, None), ("XL", 599, 402, None, None)]},
    {"brand": "Van Rysel", "model": "Triban RC 120", "years": "2018–2025", "sizes": [
        ("XS", 539, 376, None, None), ("S", 555, 376, None, None), ("M", 580, 376, None, None),
        ("L", 611, 383, None, None), ("XL", 640, 385, None, None)]},
    {"brand": "Van Rysel", "model": "Triban RC 500 / RC 520", "years": "2018–2025", "sizes": [
        ("XS", 524, 375, None, None), ("S", 542, 380, None, None), ("M", 569, 379, None, None),
        ("L", 603, 385, None, None), ("XL", 633, 386, None, None)]},
    {"brand": "Van Rysel", "model": "Ultra CF", "years": "2019–2022", "sizes": [
        ("XS", 516, 382, None, None), ("S", 532, 388, None, None), ("M", 548, 398, None, None),
        ("L", 572, 401, None, None), ("XL", 596, 403, None, None)]},
    {"brand": "Wilier", "model": "Cento10 NDR", "years": "2018–2022", "sizes": [
        ("XS", 527, 369, None, None), ("S", 546, 374, None, None), ("M", 566, 379, None, None),
        ("L", 586, 384, None, None), ("XL", 604, 389, None, None), ("XXL", 625, 395, None, None)]},
    {"brand": "Wilier", "model": "Filante SLR", "years": "2021–2025", "sizes": [
        ("XS", 505, 380, None, None), ("S", 521, 384, None, None), ("M", 538, 388, None, None),
        ("L", 555, 391, None, None), ("XL", 571, 395, None, None), ("XXL", 587, 399, None, None)]},
    {"brand": "Wilier", "model": "Zero SLR", "years": "2020–2025", "sizes": [
        ("XS", 503, 376, None, None), ("S", 519, 381, None, None), ("M", 536, 386, None, None),
        ("L", 554, 391, None, None), ("XL", 572, 397, None, None), ("XXL", 591, 402, None, None)]},
]


def presets() -> list[dict]:
    """PRESETS with each size as a dict, ready for JSON."""
    out = []
    for i, p in enumerate(PRESETS):
        sizes = [{"size": g, "stack_mm": s, "reach_mm": r, "seat_angle_deg": a, "crank_mm": k}
                 for g, s, r, a, k in p["sizes"]]
        out.append({"id": i, "brand": p["brand"], "model": p["model"], "years": p["years"], "sizes": sizes})
    return out
