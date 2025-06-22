# toolkit_logic.py - CORRECTED AND FINAL VERSION
import pandas as pd
from typing import Dict, List, Union, Optional, Tuple
import json
from datetime import datetime
import logging
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SDGAssessmentToolkit:
    """
    Enhanced SDG Assessment Toolkit for Architecture Projects
    Designed for UIA (Architects International Union) executives
    """
    
    def __init__(self):
        self.sdg_questions = self._load_sdg_questions()
        self.sdg_info = self._load_sdg_info()
        self.sdg_to_category_map = self._load_category_mapping()
        self.recommendations_map = self._load_recommendations()
        self.certification_references = self._load_certification_references()
        
        self.performance_levels = {
            'Exemplary': {'min': 9, 'max': 10, 'color': '#28a745'},
            'Advanced': {'min': 6, 'max': 8.99, 'color': '#90ee90'},
            'Basic': {'min': 3, 'max': 5.99, 'color': '#ffc107'},
            'Minimal': {'min': 0.1, 'max': 2.99, 'color': '#dc3545'},
            'No Score': {'min': 0, 'max': 0, 'color': '#F1FAEE'}
        }
        
        self.sdg_synergy_map = {
            1: [7, 10, 11], 2: [3, 12, 15], 3: [4, 11, 16],
            6: [3, 11, 14], 7: [1, 9, 13], 8: [1, 9, 12],
            11: [3, 10, 13], 12: [8, 13, 15], 13: [7, 11, 15]
        }

    # ... (All _load_... methods remain unchanged from your version) ...
    def _load_sdg_questions(self) -> Dict:
        # This data remains the same as in your original file.
        return {
            "1: Basic Needs & Economy": [
                {
                    "id": "q1", 
                    "sdg_id": 1, 
                    "text": "1. How does your project address operational cost burdens for occupants compared to regional standards?", 
                    "type": "radio", 
                    "weight": 1.0,
                    "options": {
                        "Not applicable to this project": 0,
                        "Implements basic efficiency measures with modest cost reduction (~10-15%)": 1,
                        "Incorporates advanced systems reducing operational costs by approximately 30-40%": 2,
                        "Features comprehensive efficiency strategies reducing costs by approximately 50-60%": 3,
                        "Achieves near-zero operational costs through integrated passive and active systems": 4,
                        "Generates surplus resources (energy, water, etc.) that provide economic benefit to occupants": 5
                    }
                },
                {
                    "id": "q2", 
                    "sdg_id": 1, 
                    "text": "2. To what extent does your project enhance economic resilience for its users and the surrounding community?", 
                    "type": "checkbox", 
                    "weight": 1.0,
                    "options": {
                        "Incorporates spaces that support income-generating activities": 1,
                        "Reduces transportation costs through location or connectivity features": 1,
                        "Provides flexible spaces adaptable to changing economic conditions": 1,
                        "Includes infrastructure resilient to environmental/economic disruptions": 1,
                        "Offers tiered affordability options for diverse economic circumstances": 1
                    }
                },
                {
                    "id": "q3", 
                    "sdg_id": 2, 
                    "text": "3. How does your project incorporate productive landscape elements that enhance local food systems?", 
                    "type": "radio", 
                    "weight": 1.0,
                    "options": {
                        "Not applicable to this project": 0,
                        "Basic consideration with no dedicated productive spaces": 1,
                        "Allocation of shared green spaces for future conversion": 2,
                        "Integration of designated community garden spaces": 3,
                        "Comprehensive productive landscape strategy": 4,
                        "Full food system integration (production, processing, distribution)": 5
                    }
                },
                {
                    "id": "q4", 
                    "sdg_id": 2, 
                    "text": "4. To what extent does your project address the complete food cycle and contribute to local food system resilience?", 
                    "type": "checkbox", 
                    "weight": 1.0,
                    "options": {
                        "Incorporates composting infrastructure": 1,
                        "Provides appropriate food storage and preservation spaces": 1,
                        "Includes design elements that extend growing seasons": 1,
                        "Features water collection/irrigation systems for food production": 1,
                        "Allocates spaces for food education and skill-building": 1
                    }
                }
            ],
            "2: Health & Education": [
                {
                    "id": "q5", 
                    "sdg_id": 3, 
                    "text": "5. How comprehensively does your project incorporate design elements that support mental health and psychological well-being?", 
                    "type": "checkbox", 
                    "weight": 1.0,
                    "options": {
                        "Biophilic design elements (natural elements, materials, patterns)": 1,
                        "Spaces for mindfulness, meditation, or quiet reflection": 1,
                        "Access to quality daylighting": 1,
                        "Views to nature or green spaces": 1,
                        "Design fostering social connection while respecting privacy": 1
                    }
                },
                {
                    "id": "q6", 
                    "sdg_id": 3, 
                    "text": "6. To what extent does your project's design actively promote physical activity and healthy behaviors?", 
                    "type": "radio", 
                    "weight": 1.0,
                    "options": {
                        "Not applicable to this project": 0,
                        "Meets basic accessibility with limited active design": 1,
                        "Incorporates some passive strategies (e.g., visible stairs)": 2,
                        "Features dedicated spaces for physical activity": 3,
                        "Comprehensive active design with connected indoor-outdoor spaces": 4,
                        "Fully integrated health-promoting design with programming and monitoring": 5
                    }
                },
                {
                    "id": "q7", 
                    "sdg_id": 4, 
                    "text": "7. How comprehensively does your project address inclusive design principles for diverse users in learning-oriented spaces?", 
                    "type": "checkbox", 
                    "weight": 1.0,
                    "options": {
                        "Mobility accessibility (beyond code requirements)": 1,
                        "Visual accessibility (wayfinding, signage)": 1,
                        "Auditory accessibility (acoustics, listening systems)": 1,
                        "Cognitive/neurodiversity considerations": 1,
                        "Flexible learning environments": 1
                    }
                },
                {
                    "id": "q8", 
                    "sdg_id": 4, 
                    "text": "8. To what extent does your project incorporate spaces that facilitate knowledge sharing and lifelong learning?", 
                    "type": "radio", 
                    "weight": 1.0,
                    "options": {
                        "Not applicable to this project": 0,
                        "Basic information display areas": 1,
                        "Dedicated spaces for structured learning": 2,
                        "Integrated formal and informal learning zones": 3,
                        "Comprehensive learning ecosystem with community connections": 4,
                        "Innovation-focused environment supporting experimentation": 5
                    }
                }
            ],
            "3: Inclusion & Water": [
                {
                    "id": "q9", 
                    "sdg_id": 5, 
                    "text": "9. How comprehensively does your project implement equitable team composition and workplace practices?", 
                    "type": "checkbox", 
                    "weight": 1.0,
                    "options": {
                        "Diverse design team with gender representation": 1,
                        "Equitable compensation structures": 1,
                        "Procurement policies prioritizing diverse contractors": 1,
                        "Site management practices supporting diverse construction roles": 1,
                        "Equitable leadership opportunities": 1
                    }
                },
                {
                    "id": "q10", 
                    "sdg_id": 5, 
                    "text": "10. To what extent does your project's design address diverse user needs across gender identities?", 
                    "type": "radio", 
                    "weight": 1.0,
                    "options": {
                        "Not applicable to this project": 0,
                        "Basic code compliance": 1,
                        "Initial stakeholder analysis includes gender data": 2,
                        "Intentional design features for diverse user needs": 3,
                        "Comprehensive user-centered design with balanced representation": 4,
                        "Transformative approach challenging traditional gender assumptions": 5
                    }
                },
                {
                    "id": "q11", 
                    "sdg_id": 6, 
                    "text": "11. How comprehensively does your project address water efficiency and conservation?", 
                    "type": "radio", 
                    "weight": 1.0,
                    "options": {
                        "Not applicable to this project": 0,
                        "Basic compliance with conventional fixtures": 1,
                        "Moderate reduction with low-flow fixtures and rainwater collection": 2,
                        "Advanced management with greywater reuse": 3,
                        "Comprehensive strategy achieving 50%+ reduction": 4,
                        "Net-positive water approach contributing to watershed health": 5
                    }
                },
                {
                    "id": "q12", 
                    "sdg_id": 6, 
                    "text": "12. Which strategies does your project implement to protect water quality and manage the complete water cycle?", 
                    "type": "checkbox", 
                    "weight": 1.0,
                    "options": {
                        "Construction-phase protections (pollutant discharge)": 1,
                        "Stormwater management with filtration": 1,
                        "Potable water quality assurance": 1,
                        "Ecosystem protection/restoration of water features": 1,
                        "Long-term maintenance protocols for water systems": 1
                    }
                }
            ],
            "4: Energy & Resources": [
                {
                    "id": "q13", 
                    "sdg_id": 7, 
                    "text": "13. How comprehensively does your project incorporate renewable energy systems and energy efficiency?", 
                    "type": "radio", 
                    "weight": 1.0,
                    "options": {
                        "Not applicable to this project": 0,
                        "Basic energy code compliance": 1,
                        "Moderate efficiency (25-30% better) with some renewables": 2,
                        "Advanced performance (40-50% better) with significant renewables": 3,
                        "Near net-zero energy performance": 4,
                        "Net-positive energy building": 5
                    }
                },
                {
                    "id": "q14", 
                    "sdg_id": 7, 
                    "text": "14. To what extent does your project address energy resilience, affordability, and accessibility?", 
                    "type": "checkbox", 
                    "weight": 1.0,
                    "options": {
                        "Passive design for power outages": 1,
                        "Systems reducing operational costs": 1,
                        "Distributed energy resources for grid reliability": 1,
                        "Energy monitoring and smart systems": 1,
                        "Features ensuring equitable energy access": 1
                    }
                },
                {
                    "id": "q15", 
                    "sdg_id": 8, 
                    "text": "15. How comprehensively does your project support local economic development and fair labor practices?", 
                    "type": "radio", 
                    "weight": 1.0,
                    "options": {
                        "Not applicable to this project": 0,
                        "Basic compliance with labor standards": 1,
                        "Implementation of fair labor practices with some local preference": 2,
                        "Structured involvement of local SMEs": 3,
                        "Comprehensive local economic strategy": 4,
                        "Transformative approach with full integration of local enterprises/labor": 5
                    }
                },
                {
                    "id": "q16", 
                    "sdg_id": 12, 
                    "text": "16. To what extent does your project incorporate life cycle thinking and resource efficiency in materials?", 
                    "type": "checkbox", 
                    "weight": 1.0,
                    "options": {
                        "Comprehensive Life Cycle Assessment (LCA) conducted": 1,
                        "Preference for locally-sourced materials": 1,
                        "Selection based on renewable resource management": 1,
                        "Durability and maintenance factored into selection": 1,
                        "Incorporation of recycled/salvaged materials": 1
                    }
                }
            ],
            "5: Infrastructure & Innovation": [
                {
                    "id": "q17", 
                    "sdg_id": 9, 
                    "text": "17. How does your project approach infrastructure resilience and resource efficiency?", 
                    "type": "checkbox", 
                    "weight": 1.0,
                    "options": {
                        "Integration of shared infrastructure": 1,
                        "Renovation or adaptive reuse of existing buildings": 1,
                        "Implementation of smart technologies for optimization": 1,
                        "Design features enhancing climate resilience": 1,
                        "Systems reducing operational costs while maintaining service": 1
                    }
                },
                {
                    "id": "q18", 
                    "sdg_id": 9, 
                    "text": "18. To what extent does your project incorporate innovative construction approaches?", 
                    "type": "radio", 
                    "weight": 1.0,
                    "options": {
                        "Not applicable to this project": 0,
                        "Standard construction methods": 1,
                        "Established sustainable techniques adapted to local context": 2,
                        "Innovative processes improving resource efficiency": 3,
                        "Development and testing of new building systems": 4,
                        "Transformative approach combining technical innovation with local development": 5
                    }
                },
                {
                    "id": "q19", 
                    "sdg_id": 10, 
                    "text": "19. How comprehensively does your project incorporate universal design principles for equitable access?", 
                    "type": "checkbox", 
                    "weight": 1.0,
                    "options": {
                        "Barrier-free circulation systems (beyond code)": 1,
                        "Sensory accessibility features (visual, tactile, acoustic)": 1,
                        "Adaptable spaces for different abilities and ages": 1,
                        "Design elements reflecting diverse cultural identities": 1,
                        "Technology integration enhancing usability": 1
                    }
                },
                {
                    "id": "q20", 
                    "sdg_id": 10, 
                    "text": "20. To what extent does your project address socioeconomic barriers?", 
                    "type": "radio", 
                    "weight": 1.0,
                    "options": {
                        "Not applicable to this project": 0,
                        "Basic compliance with inclusivity standards": 1,
                        "At least one specific mechanism for economic accessibility": 2,
                        "Mixed-use/mixed-income approach with multiple tenure options": 3,
                        "Comprehensive inclusion strategy with affordability targets": 4,
                        "Transformative approach addressing systemic barriers": 5
                    }
                }
            ],
            "6: Sustainable Cities & Environment": [
                {
                    "id": "q21", 
                    "sdg_id": 11, 
                    "text": "21. How comprehensively does your project address key dimensions of urban sustainability?", 
                    "type": "checkbox", 
                    "weight": 1.0,
                    "options": {
                        "Affordable housing with universal design and green space access": 1,
                        "Multi-hazard resilience measures": 1,
                        "Resource-efficient systems (waste, water, energy)": 1,
                        "Preservation of cultural/natural heritage": 1,
                        "Inclusive public spaces for diverse groups": 1
                    }
                },
                {
                    "id": "q22", 
                    "sdg_id": 11, 
                    "text": "22. To what extent does your project balance immediate needs with long-term resilience?", 
                    "type": "radio", 
                    "weight": 1.0,
                    "options": {
                        "Not applicable to this project": 0,
                        "Basic compliance with minimum standards": 1,
                        "Moderate implementation of sustainable features beyond code": 2,
                        "Integrated approach with clear resilience benefits": 3,
                        "Comprehensive sustainability framework (social, environmental, economic)": 4,
                        "Transformative model demonstrating innovative approaches": 5
                    }
                },
                {
                    "id": "q23", 
                    "sdg_id": 12, 
                    "text": "23. How comprehensively does your project implement sustainable material strategies and lifecycle management?", 
                    "type": "checkbox", 
                    "weight": 1.0,
                    "options": {
                        "Integration within a recognized sustainability framework": 1,
                        "Use of certified bio-based/renewable materials": 1,
                        "Implementation of modular/adaptable systems for reuse": 1,
                        "Construction waste management plan with diversion targets": 1,
                        "Material selection prioritizing circular economy principles": 1
                    }
                },
                {
                    "id": "q24", 
                    "sdg_id": 12, 
                    "text": "24. To what extent does your project incorporate sustainable procurement and operational transparency?", 
                    "type": "radio", 
                    "weight": 1.0,
                    "options": {
                        "Not applicable to this project": 0,
                        "Basic compliance with standard procurement": 1,
                        "Selective sustainability criteria for major materials": 2,
                        "Comprehensive sustainable procurement strategy": 3,
                        "Integrated sustainability reporting with third-party verification": 4,
                        "Transformative approach with full lifecycle transparency": 5
                    }
                }
            ],
            "7: Climate & Ecosystems": [
                {
                    "id": "q25", 
                    "sdg_id": 13, 
                    "text": "25. How comprehensively does your project incorporate design strategies for climate resilience?", 
                    "type": "checkbox", 
                    "weight": 1.0,
                    "options": {
                        "Passive design for extreme temperatures": 1,
                        "Structural adaptations for natural hazards": 1,
                        "Water management for drought and flood": 1,
                        "Material selections enhancing durability": 1,
                        "Monitoring systems for environmental conditions": 1
                    }
                },
                {
                    "id": "q26", 
                    "sdg_id": 13, 
                    "text": "26. To what extent does your project implement strategies to reduce lifecycle carbon emissions?", 
                    "type": "radio", 
                    "weight": 1.0,
                    "options": {
                        "Not applicable to this project": 0,
                        "Basic efficiency with minimal embodied carbon consideration": 1,
                        "Moderate carbon reduction (20-30%)": 2,
                        "Significant reduction (40-50%)": 3,
                        "Advanced reduction (60-70%)": 4,
                        "Regenerative approach achieving net carbon negativity": 5
                    }
                },
                {
                    "id": "q27", 
                    "sdg_id": 14, 
                    "text": "27. How comprehensively does your project prevent pollutants from entering waterways?", 
                    "type": "checkbox", 
                    "weight": 1.0,
                    "options": {
                        "Comprehensive plastic waste management (construction)": 1,
                        "Limits on single-use plastic packaging for materials": 1,
                        "Material selection restricting plastic components": 1,
                        "Designated spaces for waste sorting": 1,
                        "Stormwater filtration to capture microplastics": 1
                    }
                },
                {
                    "id": "q28", 
                    "sdg_id": 14, 
                    "text": "28. To what extent does your project's design protect or enhance marine and coastal ecosystems?", 
                    "type": "radio", 
                    "weight": 1.0,
                    "options": {
                        "Not applicable to this project": 0, # Added for consistency
                        "Basic compliance with local regulations": 1,
                        "Measures to reduce construction runoff": 2,
                        "Comprehensive stormwater management with filtration": 3,
                        "Integrated water management with marine-friendly landscaping": 4,
                        "Restorative design contributing to coastal ecosystem health": 5
                    }
                },
                {
                    "id": "q29", 
                    "sdg_id": 15, 
                    "text": "29. How comprehensively does your project address terrestrial ecosystem protection?", 
                    "type": "checkbox", 
                    "weight": 1.0,
                    "options": { # Note: The values here are placeholders; the actual score is calculated by the new tiered system.
                        "Conservation/replacement of native vegetation": 1,
                        "Use of certified sustainable wood": 1,
                        "Water-sensitive landscaping": 1,
                        "Habitat preservation for local wildlife": 1,
                        "Building surface vegetation (green roofs/walls)": 1,
                        "Efficient land use (compact/reuse)": 1,
                        "Site design maintaining >40% permeable/vegetated surfaces": 1,
                        "Restoration of degraded land": 1
                    }
                },
                {
                    "id": "q30", 
                    "sdg_id": 16, 
                    "text": "30. To what extent does your project enhance safety and implement processes for fairness and transparency?", 
                    "type": "checkbox", 
                    "weight": 1.0,
                    "options": {
                        "Design enhancing perceived safety": 1,
                        "Integrated security features": 1,
                        "Documented anti-corruption procedures": 1,
                        "Transparent dispute resolution mechanisms": 1,
                        "Inclusive decision-making processes": 1,
                        "Systematic client/user feedback collection": 1,
                        "Implementation of ethical standards/certifications": 1
                    }
                },
                {
                    "id": "q31", 
                    "sdg_id": 17, 
                    "text": "31. How extensively does your project engage in partnership-building and knowledge-sharing?", 
                    "type": "checkbox", 
                    "weight": 1.0,
                    "options": {
                        "Integration within a formal cooperation program": 1,
                        "Compliance with national/regional frameworks": 1,
                        "Public dissemination of data/innovations": 1,
                        "Formation of new cross-sector partnerships": 1,
                        "Assembly of a multidisciplinary team for sustainability": 1,
                        "Contribution of performance data to databases": 1,
                        "Technology or knowledge transfer": 1,
                        "Participation in industry transformation initiatives": 1
                    }
                }
            ]
        }
    def _load_sdg_info(self) -> Dict[int, Dict[str, str]]:
        # This data is correct
        return {
            1: {"name": "No Poverty", "description": "End poverty in all its forms everywhere"},
            2: {"name": "Zero Hunger", "description": "End hunger, achieve food security and improved nutrition"},
            3: {"name": "Good Health", "description": "Ensure healthy lives and promote well-being for all"},
            4: {"name": "Quality Education", "description": "Ensure inclusive and equitable quality education"},
            5: {"name": "Gender Equality", "description": "Achieve gender equality and empower all women and girls"},
            6: {"name": "Clean Water", "description": "Ensure availability and sustainable management of water"},
            7: {"name": "Affordable Energy", "description": "Ensure access to affordable, reliable, sustainable energy"},
            8: {"name": "Decent Work", "description": "Promote sustained, inclusive economic growth and employment"},
            9: {"name": "Innovation", "description": "Build resilient infrastructure, promote innovation"},
            10: {"name": "Reduced Inequalities", "description": "Reduce inequality within and among countries"},
            11: {"name": "Sustainable Cities", "description": "Make cities and human settlements inclusive and sustainable"},
            12: {"name": "Responsible Consumption", "description": "Ensure sustainable consumption and production patterns"},
            13: {"name": "Climate Action", "description": "Take urgent action to combat climate change"},
            14: {"name": "Life Below Water", "description": "Conserve and sustainably use the oceans, seas and marine resources"},
            15: {"name": "Life on Land", "description": "Protect, restore and promote terrestrial ecosystems"},
            16: {"name": "Peace & Justice", "description": "Promote peaceful and inclusive societies for sustainable development"},
            17: {"name": "Partnerships", "description": "Strengthen the means of implementation and revitalize partnerships"}
        }
    def _load_category_mapping(self) -> Dict[int, str]:
        # This data is correct
        return {
            1: 'People', 2: 'People', 3: 'People', 4: 'People', 5: 'People',
            6: 'Planet', 12: 'Planet', 13: 'Planet', 14: 'Planet', 15: 'Planet',
            7: 'Prosperity', 8: 'Prosperity', 9: 'Prosperity', 10: 'Prosperity', 11: 'Prosperity',
            16: 'Peace', 17: 'Partnership'
        }
    def _load_certification_references(self) -> Dict[str, List[str]]:
        # This data is correct
        return {
            "energy": ["LEED Energy & Atmosphere", "BREEAM Energy", "ENERGY STAR", "Passive House", "WELL Building Standard"],
            "water": ["LEED Water Efficiency", "BREEAM Water", "WaterSense", "Living Building Challenge"],
            "materials": ["LEED Materials & Resources", "BREEAM Materials", "Cradle to Cradle", "EPD (Environmental Product Declaration)"],
            "indoor_quality": ["LEED Indoor Environmental Quality", "BREEAM Health & Wellbeing", "WELL Building Standard", "FITWEL"],
            "sustainability": ["LEED", "BREEAM", "Green Star", "CASBEE", "DGNB", "Living Building Challenge"],
            "carbon": ["Carbon Trust Standard", "LEED Carbon", "Architecture 2030", "Net Zero Carbon Buildings"]
        }
    def _load_recommendations(self) -> Dict[int, Dict[str, List[str]]]:
        # This data is correct and does not need changes
        return {1:{"design":["Integrate passive solar design principles to reduce operational energy costs","Design flexible spaces that can adapt to changing economic conditions","Consider life-cycle cost analysis in material and system selection","Implement value engineering focused on long-term operational savings"],"construction":["Prioritize local contractors and suppliers to support regional economy","Implement prefabrication strategies to reduce construction costs","Establish partnerships with local workforce development programs"],"operation":["Implement energy monitoring systems for ongoing cost optimization","Design maintenance protocols that minimize long-term operational costs","Create opportunities for occupant income generation through building design"]},2:{"design":["Integrate productive landscapes (green roofs, vertical farms, food forests)","Design kitchen gardens and community food production spaces","Specify composting infrastructure and food waste management systems","Plan for seasonal growing with greenhouse or protected growing spaces"],"construction":["Install irrigation systems for food production areas","Build raised beds and soil management infrastructure","Implement greywater systems for agricultural irrigation"],"operation":["Establish community garden management protocols","Create educational programs around sustainable food systems","Monitor food production yields and system performance"]},3:{"design":["Implement biophilic design principles throughout the project","Maximize access to natural light and views to nature","Design spaces that promote physical activity and social interaction","Specify materials that support indoor air quality and occupant health"],"construction":["Use low-VOC materials and proper ventilation during construction","Implement dust control measures to protect worker health","Establish safety protocols that exceed standard requirements"],"operation":["Monitor indoor air quality and occupant satisfaction","Maintain biophilic elements and natural systems","Provide health and wellness programming for building users"]},4:{"design":["Ensure universal design principles exceed accessibility codes","Create adaptable learning environments for diverse users","Integrate technology that supports inclusive education","Design spaces that accommodate various learning styles and needs"],"construction":["Involve diverse stakeholders in construction planning","Provide training opportunities for local workers","Ensure construction site accessibility for all workers"],"operation":["Establish ongoing education and training programs","Create feedback systems for continuous improvement","Monitor accessibility and inclusion metrics"]},5:{"design":["Design gender-neutral facilities and inclusive spaces","Ensure equitable access to all building amenities","Create safe, welcoming environments for all users","Implement universal design principles throughout"],"construction":["Ensure diverse representation in construction teams","Implement equitable hiring and compensation practices","Provide training on inclusive workplace practices"],"operation":["Establish inclusive management and decision-making processes","Monitor and address any accessibility or inclusion issues","Create opportunities for diverse leadership and participation"]},6:{"design":["Implement comprehensive water efficiency strategies","Design rainwater harvesting and greywater reuse systems","Specify water-efficient fixtures and appliances","Create water-sensitive landscaping and stormwater management"],"construction":["Install water-efficient systems and fixtures","Implement construction water management practices","Establish water quality protection measures"],"operation":["Monitor water usage and system performance","Maintain water efficiency systems and landscaping","Educate occupants on water conservation practices"]},7:{"design":["Maximize on-site renewable energy generation","Implement passive design strategies for energy efficiency","Specify high-performance building envelope and systems","Design for energy resilience and grid independence"],"construction":["Install renewable energy systems and efficient equipment","Ensure proper insulation and air sealing","Implement energy monitoring and control systems"],"operation":["Monitor energy performance and optimize systems","Maintain renewable energy systems and equipment","Implement energy management and occupant engagement programs"]},8:{"design":["Prioritize local and ethical sourcing for materials and labor","Design for durability and low maintenance requirements","Create opportunities for local economic development","Implement fair labor practices throughout the project"],"construction":["Hire local workers and contractors when possible","Provide fair wages and safe working conditions","Support local supply chains and businesses"],"operation":["Maintain fair employment practices in building operations","Support local service providers and maintenance workers","Create opportunities for local economic activity"]},9:{"design":["Incorporate resilient infrastructure and smart technologies","Design for future adaptability and technological upgrades","Implement innovative construction and material strategies","Create flexible spaces that can accommodate changing needs"],"construction":["Use innovative construction methods and technologies","Implement quality control and monitoring systems","Establish partnerships with technology providers"],"operation":["Maintain and upgrade smart building systems","Monitor performance and implement improvements","Share knowledge and innovations with the industry"]},10:{"design":["Exceed accessibility standards with universal design","Create inclusive spaces for diverse user needs","Design for socio-economic diversity and affordability","Implement strategies to reduce barriers to participation"],"construction":["Ensure construction site accessibility for all workers","Provide training on inclusive practices","Support diverse workforce development"],"operation":["Maintain inclusive access and services","Monitor and address accessibility issues","Create opportunities for diverse community engagement"]},11:{"design":["Enhance connections to public transport and active mobility","Create safe, accessible, and engaging public spaces","Promote mixed-use development to reduce travel needs","Integrate green infrastructure for urban resilience"],"construction":["Minimize construction impacts on surrounding community","Implement sustainable construction practices","Support local infrastructure improvements"],"operation":["Maintain public spaces and community amenities","Monitor building impact on surrounding area","Support local community initiatives and programs"]},12:{"design":["Specify materials with high recycled content and low environmental impact","Design for deconstruction and material reuse","Implement comprehensive waste management strategies","Prioritize circular economy principles in material selection"],"construction":["Implement construction waste management and diversion","Use sustainable materials and construction practices","Establish material tracking and documentation systems"],"operation":["Maintain sustainable material management practices","Monitor material performance and durability","Implement ongoing waste reduction and recycling programs"]},13:{"design":["Conduct climate risk assessment and incorporate adaptation measures","Prioritize low-embodied carbon materials and systems","Utilize passive design strategies to reduce energy demand","Implement comprehensive carbon management strategies"],"construction":["Minimize construction carbon emissions","Use low-carbon materials and construction methods","Implement carbon monitoring and offset strategies"],"operation":["Monitor operational carbon emissions","Optimize systems for carbon reduction","Implement ongoing carbon management and reduction programs"]},14:{"design":["Implement advanced stormwater management systems","Prevent water pollution during construction and operation","Protect marine/aquatic ecosystems if near water bodies","Minimize use of materials harmful to aquatic life"],"construction":["Implement construction water quality protection measures","Install stormwater management and filtration systems","Establish water quality monitoring protocols"],"operation":["Maintain water quality protection systems","Monitor water quality and ecosystem impacts","Implement ongoing water quality management programs"]},15:{"design":["Enhance on-site biodiversity with native planting and habitat creation","Protect existing ecosystems and mature trees","Specify sustainably harvested timber and bio-based materials","Implement comprehensive ecological restoration strategies"],"construction":["Protect existing vegetation and wildlife during construction","Install native landscaping and habitat features","Establish ecological monitoring and management protocols"],"operation":["Maintain native landscaping and habitat features","Monitor biodiversity and ecosystem health","Implement ongoing ecological management and restoration"]},16:{"design":["Ensure transparent project communication and stakeholder engagement","Promote inclusive design processes and decision-making","Implement fair labor practices and ethical procurement","Establish clear governance and accountability mechanisms"],"construction":["Maintain transparent construction practices and communication","Ensure fair labor practices and worker safety","Establish clear dispute resolution and feedback mechanisms"],"operation":["Maintain transparent building operations and management","Implement ongoing stakeholder engagement and feedback","Monitor and address any governance or transparency issues"]},17:{"design":["Collaborate with local communities and sustainability experts","Share project performance data and lessons learned","Seek partnerships to enhance sustainability outcomes","Participate in industry knowledge-sharing initiatives"],"construction":["Establish partnerships with local organizations and experts","Share construction innovations and best practices","Contribute to industry knowledge and capacity building"],"operation":["Maintain partnerships for ongoing sustainability improvements","Share operational data and performance insights","Participate in industry transformation and knowledge sharing"]}}

    def get_performance_level(self, score: float) -> str:
        for level, limits in self.performance_levels.items():
            if limits['min'] <= score <= limits['max']:
                return level
        return 'No Score'

    def get_performance_color(self, score: float) -> str:
        level = self.get_performance_level(score)
        return self.performance_levels.get(level, {}).get('color', '#cccccc')
    
    def _calculate_architecture_metrics(self, scores_df: pd.DataFrame) -> Dict:
        metrics = {}
        if scores_df.empty:
            return {}
        energy_sdgs = [7, 13]
        energy_scores = scores_df[scores_df['SDG_ID'].isin(energy_sdgs)]['Final_Score']
        metrics['energy_performance'] = round(energy_scores.mean(), 1) if not energy_scores.empty else 0.0
        water_sdgs = [6, 14]
        water_scores = scores_df[scores_df['SDG_ID'].isin(water_sdgs)]['Final_Score']
        metrics['water_efficiency'] = round(water_scores.mean(), 1) if not water_scores.empty else 0.0
        material_sdgs = [8, 12, 15]
        material_scores = scores_df[scores_df['SDG_ID'].isin(material_sdgs)]['Final_Score']
        metrics['material_sustainability'] = round(material_scores.mean(), 1) if not material_scores.empty else 0.0
        return metrics

    def _generate_insights(self, scores_df: pd.DataFrame, category_scores: Dict, overall_score: float) -> List[str]:
        insights = []
        overall_level = self.get_performance_level(overall_score)
        if overall_level == 'Exemplary':
            insights.append(f"🌟 Exemplary Overall Performance ({overall_score:.1f}/10). A leading example of sustainable architecture.")
        elif overall_level == 'Advanced':
            insights.append(f"👍 Advanced Overall Performance ({overall_score:.1f}/10). Strong alignment with key sustainability goals.")
        elif overall_level == 'Basic':
            insights.append(f"✅ Basic Overall Performance ({overall_score:.1f}/10). A good foundation with clear areas for improvement.")
        else:
            insights.append(f"🎯 Minimal Overall Performance ({overall_score:.1f}/10). Significant opportunities for enhancement.")
        best_category = max(category_scores.keys(), key=lambda k: category_scores[k]['Final_Score'])
        worst_category = min(category_scores.keys(), key=lambda k: category_scores[k]['Final_Score'])
        if best_category != worst_category:
            insights.append(f"💪 Strongest area: '{best_category}' with an average score of {category_scores[best_category]['Final_Score']:.1f}/10.")
            insights.append(f"🔧 Priority area: '{worst_category}' with an average score of {category_scores[worst_category]['Final_Score']:.1f}/10.")
        if 'Bonus_Points' in scores_df.columns and scores_df['Bonus_Points'].sum() > 0:
            bonus_sum = scores_df['Bonus_Points'].sum()
            insights.append(f"🔄 Strong Synergy! Your project earned {bonus_sum:.1f} total bonus points from high performance in interconnected SDGs.")
        return insights[:5] 

    # ... (Other helper methods like get_..._recommendations, get_all_questions remain unchanged) ...
    def get_phase_specific_recommendations(self, sdg_id: int, phase: str = "design") -> List[str]:
        sdg_recommendations = self.recommendations_map.get(sdg_id, {})
        if isinstance(sdg_recommendations, dict):
            return sdg_recommendations.get(phase, [])
        return []
    def get_all_phase_recommendations(self, sdg_id: int) -> Dict[str, List[str]]:
        sdg_recommendations = self.recommendations_map.get(sdg_id, {})
        if isinstance(sdg_recommendations, dict):
            return sdg_recommendations
        return {"design": [], "construction": [], "operation": []}
    def validate_responses(self, responses: Dict) -> Tuple[bool, List[str]]:
        errors = []
        all_questions = self.get_all_questions()
        if not responses:
            errors.append("No responses provided")
            return False, errors
        answered_q_ids = {k for k, v in responses.items() if v}
        if not answered_q_ids:
            errors.append("No questions have been answered.")
            return False, errors
        return True, []
    def get_all_questions(self) -> Dict:
        all_questions = {}
        for section_questions in self.sdg_questions.values():
            for question in section_questions:
                all_questions[question['id']] = question
        return all_questions
    def get_questions_by_sdg(self, sdg_id: int) -> List[Dict]:
        questions = []
        for section_questions in self.sdg_questions.values():
            for question in section_questions:
                if question['sdg_id'] == sdg_id:
                    questions.append(question)
        return questions
        
    def calculate_max_scores(self) -> Dict[int, float]:
        """Calculate maximum possible scores for each SDG"""
        sdg_max_scores = {}
        all_questions = self.get_all_questions()
        
        for q_id, question in all_questions.items():
            sdg_id = question['sdg_id']
            weight = question.get('weight', 1.0)
            
            if sdg_id not in sdg_max_scores:
                sdg_max_scores[sdg_id] = 0
            
            valid_options = {k: v for k, v in question['options'].items() if "not applicable" not in k.lower()}

            if question['type'] == 'radio':
                max_score = max(valid_options.values()) if valid_options else 0
            elif question['type'] == 'checkbox':
                # MODIFIED: For tiered questions, max score is always 5.
                if q_id in ['q29', 'q30', 'q31']:
                    max_score = 5
                else:
                    max_score = sum(valid_options.values()) if valid_options else 0
            else:
                max_score = 0
            
            sdg_max_scores[sdg_id] += max_score * weight
        
        return sdg_max_scores
    
    # NEW HELPER FUNCTION: To calculate score for tiered checkbox questions
    def _calculate_tiered_score(self, num_checked: int, tiers: Dict[Tuple[int, int], int]) -> int:
        """Calculates score based on the number of checked items and defined tiers."""
        for (lower_bound, upper_bound), score in tiers.items():
            if lower_bound <= num_checked <= upper_bound:
                return score
        return 0

    def calculate_raw_scores(self, responses: Dict) -> Dict[int, float]:
        """Calculate raw scores for each SDG based on responses"""
        sdg_scores = {}
        all_questions = self.get_all_questions()

        # MODIFIED: Define the scoring tiers from the reference document
        q29_tiers = {(0, 1): 1, (2, 3): 2, (4, 5): 3, (6, 7): 4, (8, 8): 5}
        q30_tiers = {(0, 1): 1, (2, 3): 2, (4, 5): 3, (6, 6): 4, (7, 7): 5}
        q31_tiers = {(0, 1): 1, (2, 3): 2, (4, 5): 3, (6, 7): 4, (8, 8): 5}
        
        for q_id, response in responses.items():
            if q_id not in all_questions or not response:
                continue
            
            question = all_questions[q_id]
            sdg_id = question['sdg_id']
            weight = question.get('weight', 1.0)
            
            if sdg_id not in sdg_scores:
                sdg_scores[sdg_id] = 0
            
            # MODIFIED: Logic to handle both linear and tiered checkboxes
            if question['type'] == 'checkbox':
                if isinstance(response, list):
                    num_checked = len(response)
                    score = 0
                    if q_id == 'q29':
                        score = self._calculate_tiered_score(num_checked, q29_tiers)
                    elif q_id == 'q30':
                        score = self._calculate_tiered_score(num_checked, q30_tiers)
                    elif q_id == 'q31':
                        score = self._calculate_tiered_score(num_checked, q31_tiers)
                    else: # Original linear scoring for all other checkboxes
                        for item in response:
                            if item in question['options']:
                                score += question['options'][item]
                    sdg_scores[sdg_id] += score * weight

            elif question['type'] == 'radio' and response in question['options']:
                sdg_scores[sdg_id] += question['options'][response] * weight
        
        return sdg_scores
    
    def calculate_assessment_results(self, responses: Dict) -> Dict:
        """
        Calculates assessment results using the 0-10 scale and synergy bonus points.
        (This function is now fully aligned with the reference)
        """
        try:
            is_valid, errors = self.validate_responses(responses)
            if not is_valid:
                return {"error": "Invalid responses", "details": errors}

            raw_scores = self.calculate_raw_scores(responses)
            max_scores = self.calculate_max_scores()
            direct_scores = {}
            for sdg_id in self.sdg_info.keys(): # Iterate over all SDGs to include those with 0 score
                if max_scores.get(sdg_id, 0) > 0:
                    score_10_scale = (raw_scores.get(sdg_id, 0) / max_scores[sdg_id]) * 10
                    direct_scores[sdg_id] = round(score_10_scale, 2)
                else:
                    direct_scores[sdg_id] = 0

            bonus_points = {sdg_id: 0 for sdg_id in self.sdg_info}
            for source_sdg, source_score in direct_scores.items():
                if source_sdg not in self.sdg_synergy_map:
                    continue
                bonus_value = 0
                if 7 <= source_score < 8: bonus_value = 0.5
                elif 8 <= source_score < 9: bonus_value = 0.7
                elif source_score >= 9: bonus_value = 1.0
                if bonus_value > 0:
                    for recipient_sdg in self.sdg_synergy_map[source_sdg]:
                        if bonus_points.get(recipient_sdg, 0) < 2.0:
                            current_bonus = bonus_points.get(recipient_sdg, 0)
                            potential_add = min(bonus_value, 2.0 - current_bonus)
                            bonus_points[recipient_sdg] = round(current_bonus + potential_add, 2)
            
            results_data = []
            # Make sure to process all SDGs, even if they had no direct score initially
            answered_sdgs = set(direct_scores.keys())
            all_sdgs = set(self.sdg_info.keys())
            for sdg_id in sorted(list(answered_sdgs)):
                direct = direct_scores.get(sdg_id, 0)
                bonus = bonus_points.get(sdg_id, 0)
                final_score = min(10.0, direct + bonus)
                performance = self.get_performance_level(final_score)
                
                results_data.append({
                    "SDG_ID": sdg_id,
                    "SDG_Name_Short": self.sdg_info[sdg_id]["name"],
                    "Direct_Score": direct,
                    "Bonus_Points": bonus,
                    "Final_Score": round(final_score, 1),
                    "Performance": performance,
                    "Performance_Color": self.get_performance_color(final_score),
                    "Category": self.sdg_to_category_map[sdg_id]
                })

            if not results_data:
                return {"error": "No scores could be calculated from the provided responses."}

            scores_df = pd.DataFrame(results_data)
            
            category_scores = scores_df.groupby('Category').agg(Final_Score=('Final_Score', 'mean')).round(1).to_dict('index')
            for cat, data in category_scores.items():
                data['Performance'] = self.get_performance_level(data['Final_Score'])
                data['Performance_Color'] = self.get_performance_color(data['Final_Score'])

            overall_score = round(scores_df['Final_Score'].mean(), 1) if not scores_df.empty else 0.0
            
            sorted_df = scores_df.sort_values(by='Final_Score', ascending=False)
            strengths = sorted_df.head(5).to_dict('records')
            weaknesses = sorted_df[sorted_df['Final_Score'] < 6].tail(5).sort_values('Final_Score').to_dict('records')
            
            performance_distribution = scores_df['Performance'].value_counts().to_dict()
            insights = self._generate_insights(scores_df, category_scores, overall_score)
            
            return {
                "scores_df": scores_df,
                "category_scores": category_scores,
                "overall_score": overall_score,
                "strengths": strengths,
                "weaknesses": weaknesses,
                "insights": insights,
                "performance_distribution": performance_distribution,
                "architecture_metrics": self._calculate_architecture_metrics(scores_df),
                "assessment_date": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Error calculating assessment results: {str(e)}", exc_info=True)
            return {"error": f"Calculation error: {str(e)}"}
            
    def export_results_to_json(self, results: Dict, filepath: str = None) -> str:
        try:
            export_data = results.copy()
            if 'scores_df' in export_data and isinstance(export_data['scores_df'], pd.DataFrame):
                export_data['scores_df'] = export_data['scores_df'].to_dict('records')
            json_str = json.dumps(export_data, indent=2, ensure_ascii=False, default=str)
            if filepath:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(json_str)
                logger.info(f"Results exported to {filepath}")
            return json_str
        except Exception as e:
            logger.error(f"Error exporting results: {str(e)}")
            return ""

# This remains for potential direct script usage, but is not used by the Streamlit app
_toolkit_instance = SDGAssessmentToolkit()