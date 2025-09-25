#!/usr/bin/env python3
"""Create 20 diverse, realistic Tonkin project samples for testing."""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from database import KnowledgeDatabase

def create_expanded_projects():
    """Create 20 diverse project documents for testing."""
    
    # Diverse project data across Australian states and disciplines
    projects = [
        {
            "project_name": "Adelaide Hills Stormwater Detention Basin",
            "project_number": "TKN-2024-SW-001",
            "program_region": "South Australia",
            "category": "Stormwater Management",
            "project_leader": "Sarah Mitchell",
            "project_reviewer": "David Chen",
            "lead_disciplines": "Hydraulic Engineering, Environmental",
            "client": "Adelaide Hills Council",
            "client_representative": "Mark Thompson",
            "background": "The Adelaide Hills Council requires a new detention basin to manage stormwater runoff from expanding residential development in Mount Barker. Current infrastructure inadequate for increased flow volumes.",
            "scope_of_work": "Design and construct 50,000m³ detention basin with inlet/outlet structures, landscaping, and environmental controls. Include flood modeling and environmental impact assessment.",
            "scope_of_services": "Hydraulic modeling, detailed design, environmental assessment, construction documentation, construction supervision, commissioning support.",
            "deliverables": "Hydraulic model report, Design drawings (civil, structural, electrical), Environmental management plan, Construction specifications, As-built documentation",
            "reference_documents": "Australian Rainfall & Runoff Guidelines 2019, SA Planning Code, Council Development Standards, Flood mapping data from DEW",
            "assumptions": "Site access available during construction, No contaminated materials expected, Standard soil conditions per geotechnical report",
            "performance_requirements": "1:100 year ARI flood protection, Environmental flow releases, Maximum 2m/s outlet velocity, Native vegetation retention >80%",
            "trust_score": 0.95,
            "days_old": 45
        },
        {
            "project_name": "Pacific Highway Bridge Replacement",
            "project_number": "TKN-2024-BD-003",
            "program_region": "New South Wales",
            "category": "Bridge Design",
            "project_leader": "Michael Rodriguez",
            "project_reviewer": "Jennifer Walsh",
            "lead_disciplines": "Structural Engineering, Traffic Engineering",
            "client": "Transport for NSW",
            "client_representative": "Lisa Wang",
            "background": "Existing concrete bridge over Hawkesbury River built in 1962 requires replacement due to structural deterioration and inadequate capacity for current traffic loads.",
            "scope_of_work": "Replace existing 2-lane bridge with new 4-lane structure including pedestrian/cyclist facilities. Maintain traffic flow during construction.",
            "scope_of_services": "Structural design, traffic management planning, environmental approvals, detailed documentation, construction support",
            "deliverables": "Bridge design drawings, Structural calculations, Traffic management plan, Environmental assessment, Construction methodology",
            "reference_documents": "AS 5100 Bridge Design Code, TfNSW Bridge Design Manual, Geotechnical investigation report, Traffic count data",
            "assumptions": "Marine construction access available, Standard foundation conditions, No heritage constraints identified",
            "performance_requirements": "100-year design life, T44 loading, 80km/h design speed, 3.5m lane widths, Flood immunity to 1:100 ARI",
            "trust_score": 0.88,
            "days_old": 75
        },
        {
            "project_name": "Perth Water Treatment Plant Upgrade",
            "project_number": "TKN-2023-WT-007",
            "program_region": "Western Australia",
            "category": "Water Treatment",
            "project_leader": "Emma Thompson",
            "project_reviewer": "Robert Kim",
            "lead_disciplines": "Process Engineering, Chemical Engineering, Mechanical",
            "client": "Water Corporation WA",
            "client_representative": "Andrew Stevens",
            "background": "Existing water treatment plant requires capacity upgrade from 50ML/d to 80ML/d to meet growing demand in Perth northern suburbs. New advanced treatment processes required.",
            "scope_of_work": "Design and construct additional treatment trains including coagulation, flocculation, sedimentation, filtration and disinfection systems.",
            "scope_of_services": "Process design, mechanical/electrical design, control system integration, commissioning support, operator training",
            "deliverables": "Process flow diagrams, Equipment specifications, Control philosophy, Commissioning procedures, O&M manuals",
            "reference_documents": "NHMRC Australian Drinking Water Guidelines, AS/NZS 4020, Water Corp design standards, Existing plant O&M data",
            "assumptions": "Existing intake capacity adequate, Power supply upgrade available, Skilled operators available for training",
            "performance_requirements": "Water quality compliance to ADWG, 99.5% availability, Energy efficiency targets, Automated control systems",
            "trust_score": 0.92,
            "days_old": 120
        },
        {
            "project_name": "Melbourne Metro Rail Tunnel Geotechnical Assessment",
            "project_number": "TKN-2024-GT-015",
            "program_region": "Victoria",
            "category": "Geotechnical Engineering",
            "project_leader": "Dr. Priya Sharma",
            "project_reviewer": "Simon Roberts",
            "lead_disciplines": "Geotechnical Engineering, Rock Engineering",
            "client": "Melbourne Metro Tunnel Authority",
            "client_representative": "James Mitchell",
            "background": "Comprehensive geotechnical investigation for 9km twin-bore tunnels under Melbourne CBD. Critical for TBM selection and tunnel design parameters.",
            "scope_of_work": "Geotechnical characterization of tunnel alignment including soil/rock properties, groundwater conditions, and settlement predictions.",
            "scope_of_services": "Site investigation planning, drilling supervision, laboratory testing, geotechnical modeling, design parameter recommendations",
            "deliverables": "Geotechnical investigation report, Ground model, Settlement predictions, TBM recommendations, Tunneling methodology",
            "reference_documents": "AS 4133 Rock and Soil Testing, ITA guidelines, Previous Melbourne tunnel reports, Geological survey data",
            "assumptions": "Access permits obtained, Utility clearances available, Standard tunneling methods applicable",
            "performance_requirements": "Settlement limits <25mm, Rock mass classification, Groundwater ingress predictions, TBM performance criteria",
            "trust_score": 0.96,
            "days_old": 60
        },
        {
            "project_name": "Brisbane Airport Runway Extension",
            "project_number": "TKN-2024-AV-008",
            "program_region": "Queensland",
            "category": "Aviation Infrastructure",
            "project_leader": "Captain Alex Turner",
            "project_reviewer": "Maria Gonzalez",
            "lead_disciplines": "Aviation Engineering, Pavement Design, Electrical",
            "client": "Brisbane Airport Corporation",
            "client_representative": "Rachel Green",
            "background": "Extension of main runway from 3,560m to 4,000m to accommodate A380 and future aircraft. Includes taxiway modifications and lighting upgrades.",
            "scope_of_work": "Design runway extension with associated taxiways, drainage, lighting, and navigation aids. Maintain airport operations during construction.",
            "scope_of_services": "Pavement design, airfield lighting, navigation systems, construction phasing, safety assessments",
            "deliverables": "Pavement design report, Lighting design, Navigation aid specifications, Construction staging plan, Safety case",
            "reference_documents": "CASA Manual of Standards Part 139, ICAO Annex 14, Airport technical standards, Geotechnical reports",
            "assumptions": "CASA approvals obtained, Aircraft operations coordination available, Standard materials procurement",
            "performance_requirements": "Code F aircraft capability, 25-year pavement life, CAT III approach lighting, Environmental noise compliance",
            "trust_score": 0.89,
            "days_old": 90
        },
        {
            "project_name": "Darwin Port Marine Infrastructure Upgrade",
            "project_number": "TKN-2024-MR-012",
            "program_region": "Northern Territory",
            "category": "Marine Engineering",
            "project_leader": "Captain James Harrison",
            "project_reviewer": "Dr. Sarah Ocean",
            "lead_disciplines": "Marine Engineering, Structural Engineering, Environmental",
            "client": "Darwin Port Corporation",
            "client_representative": "Michael Tran",
            "background": "Upgrade existing wharf structures to handle larger vessels and increased cargo capacity. Critical for northern Australia trade growth.",
            "scope_of_work": "Strengthen existing wharfs, construct new berth, upgrade cranes and container handling facilities. Include dredging and environmental works.",
            "scope_of_services": "Marine structural design, dredging design, environmental impact assessment, construction methodology, marine operations planning",
            "deliverables": "Wharf design drawings, Dredging specifications, Environmental management plan, Construction methodology, Marine safety procedures",
            "reference_documents": "AS 4997 Marine Structures, Port design guidelines, Environmental regulations, Tidal and wave data",
            "assumptions": "Dredging permits available, Marine access maintained, Standard pile driving conditions",
            "performance_requirements": "50-year design life, Cyclone resistance, Environmental compliance, Operational efficiency targets",
            "trust_score": 0.94,
            "days_old": 30
        },
        {
            "project_name": "Hobart Waste Management Facility",
            "project_number": "TKN-2023-WM-019",
            "program_region": "Tasmania",
            "category": "Waste Management",
            "project_leader": "Dr. Rebecca Green",
            "project_reviewer": "Ian McDermott",
            "lead_disciplines": "Environmental Engineering, Process Engineering",
            "client": "City of Hobart",
            "client_representative": "Tom Wilson",
            "background": "New integrated waste management facility including materials recovery, organic processing, and residual waste treatment. Zero waste to landfill target.",
            "scope_of_work": "Design integrated facility for 100,000 tonnes/year capacity including sorting, composting, anaerobic digestion, and energy recovery systems.",
            "scope_of_services": "Process design, facility layout, environmental approvals, waste flow modeling, technology selection",
            "deliverables": "Process design report, Facility drawings, Environmental assessment, Technology specifications, Business case",
            "reference_documents": "EPA waste guidelines, AS 4454 Composting, European waste standards, Best practice reviews",
            "assumptions": "Site zoning approved, Utility connections available, Waste supply contracts secured",
            "performance_requirements": "90% diversion from landfill, Odor compliance, Energy self-sufficiency, Economic viability",
            "trust_score": 0.87,
            "days_old": 180
        },
        {
            "project_name": "Canberra Light Rail Extension",
            "project_number": "TKN-2024-TR-025",
            "program_region": "Australian Capital Territory",
            "category": "Public Transport",
            "project_leader": "Dr. Transport Lee",
            "project_reviewer": "Anna Clarke",
            "lead_disciplines": "Transport Planning, Electrical Engineering, Civil",
            "client": "ACT Government",
            "client_representative": "David Park",
            "background": "Extension of existing light rail from Civic to Woden via Parliamentary Triangle. 12km route with 19 stations through heritage and high-security areas.",
            "scope_of_work": "Design light rail extension including tracks, stations, power systems, and integration with existing network. Heritage and security considerations.",
            "scope_of_services": "Alignment design, station design, power systems, signaling, heritage assessments, security planning",
            "deliverables": "Route design, Station architecture, Power system design, Signaling specifications, Heritage reports",
            "reference_documents": "Australian Rail Standards, Heritage guidelines, Security requirements, Previous stage reports",
            "assumptions": "Commonwealth approvals obtained, Heritage constraints managed, Utility relocations coordinated",
            "performance_requirements": "60km/h maximum speed, 99% reliability, Heritage compliance, Security clearances",
            "trust_score": 0.91,
            "days_old": 50
        },
        {
            "project_name": "Gold Coast Coastal Protection Works",
            "project_number": "TKN-2024-CP-031",
            "program_region": "Queensland",
            "category": "Coastal Engineering",
            "project_leader": "Dr. Coastal Smith",
            "project_reviewer": "Marina Waters",
            "lead_disciplines": "Coastal Engineering, Environmental, Geotechnical",
            "client": "Gold Coast City Council",
            "client_representative": "Susan Beach",
            "background": "Design coastal protection for 5km of eroding shoreline protecting residential and commercial properties. Climate change adaptation required.",
            "scope_of_work": "Design seawalls, breakwaters, and beach nourishment program. Include monitoring systems and adaptive management strategies.",
            "scope_of_services": "Coastal modeling, structure design, environmental assessment, sand nourishment design, monitoring program",
            "deliverables": "Coastal protection design, Wave modeling report, Environmental approval, Construction specifications, Monitoring plan",
            "reference_documents": "Coastal protection guidelines, Wave data, Climate projections, Environmental regulations",
            "assumptions": "Sand sources available, Environmental approvals achievable, Construction access from sea",
            "performance_requirements": "1:100 year storm protection, Environmental compliance, 50-year design life, Adaptive management capability",
            "trust_score": 0.93,
            "days_old": 70
        },
        {
            "project_name": "Hunter Valley Coal Rail Duplication",
            "project_number": "TKN-2024-RL-044",
            "program_region": "New South Wales",
            "category": "Rail Infrastructure",
            "project_leader": "Robert Rails",
            "project_reviewer": "Linda Track",
            "lead_disciplines": "Rail Engineering, Structural, Geotechnical",
            "client": "Australian Rail Track Corporation",
            "client_representative": "Mark Steel",
            "background": "Duplication of 50km single track section to increase coal export capacity. Includes 3 new bridges and 2 tunnels through challenging terrain.",
            "scope_of_work": "Design and construct second track with associated bridges, tunnels, signaling, and communications. Maintain existing operations.",
            "scope_of_services": "Track design, bridge design, tunnel design, signaling systems, construction management",
            "deliverables": "Track design drawings, Bridge designs, Tunnel specifications, Signaling design, Construction methodology",
            "reference_documents": "ARTC standards, AS 7659 Rail Infrastructure, Geotechnical reports, Existing network data",
            "assumptions": "Land acquisition completed, Environmental approvals current, Standard rail construction methods",
            "performance_requirements": "25 tonne axle loads, 80km/h operating speed, 99.5% availability, ARTC standards compliance",
            "trust_score": 0.85,
            "days_old": 100
        },
        {
            "project_name": "Perth Desalination Plant Expansion",
            "project_number": "TKN-2023-DS-055",
            "program_region": "Western Australia",
            "category": "Desalination",
            "project_leader": "Dr. Salt Water",
            "project_reviewer": "Maria Fresh",
            "lead_disciplines": "Process Engineering, Marine, Electrical",
            "client": "Water Corporation WA",
            "client_representative": "Peter Ocean",
            "background": "Expand existing desalination plant capacity from 100GL/year to 150GL/year. Energy efficiency improvements and brine management optimization required.",
            "scope_of_work": "Add third desalination train with advanced energy recovery, upgrade intake/outfall systems, optimize brine discharge.",
            "scope_of_services": "Process design, marine works design, energy optimization, environmental assessment, commissioning",
            "deliverables": "Process design package, Marine structure designs, Energy analysis, Environmental approval, Commissioning plan",
            "reference_documents": "Desalination guidelines, Marine structure standards, Energy efficiency standards, Environmental regulations",
            "assumptions": "Seawater quality within design parameters, Power supply adequate, Environmental approvals renewable",
            "performance_requirements": "3.5 kWh/m³ energy consumption, 99% availability, Environmental discharge compliance, 25-year life",
            "trust_score": 0.97,
            "days_old": 200
        },
        {
            "project_name": "Adelaide Metro Bus Rapid Transit",
            "project_number": "TKN-2024-BT-062",
            "program_region": "South Australia",
            "category": "Public Transport",
            "project_leader": "Transit Tom",
            "project_reviewer": "Bus Betty",
            "lead_disciplines": "Transport Planning, Traffic Engineering, Civil",
            "client": "Adelaide Metro",
            "client_representative": "Carol Commute",
            "background": "15km bus rapid transit corridor from city to airport with dedicated lanes, priority signaling, and modern stations.",
            "scope_of_work": "Design BRT corridor with dedicated lanes, 12 stations, depot facility, and intelligent transport systems.",
            "scope_of_services": "Corridor design, station architecture, traffic modeling, ITS design, depot planning",
            "deliverables": "Corridor design, Station designs, Traffic analysis, ITS specifications, Depot layout",
            "reference_documents": "Austroads guidelines, Public transport standards, Traffic engineering standards, Planning regulations",
            "assumptions": "Road space allocation approved, Traffic management coordinated, Technology procurement available",
            "performance_requirements": "35km/h average speed, 99% on-time performance, Accessibility compliance, 30-year life",
            "trust_score": 0.86,
            "days_old": 85
        },
        {
            "project_name": "Cairns Hospital Redevelopment Infrastructure",
            "project_number": "TKN-2024-HL-073",
            "program_region": "Queensland",
            "category": "Healthcare Infrastructure",
            "project_leader": "Dr. Healthy Build",
            "project_reviewer": "Nurse Infrastructure",
            "lead_disciplines": "Mechanical, Electrical, Structural, Fire Safety",
            "client": "Queensland Health",
            "client_representative": "Medical Manager",
            "background": "Complete infrastructure upgrade for 400-bed hospital including critical power, medical gases, fire safety, and modern clinical systems.",
            "scope_of_work": "Upgrade electrical, mechanical, fire, and communications systems while maintaining hospital operations. Include emergency power and medical gas systems.",
            "scope_of_services": "MEP design, fire safety design, medical systems, construction staging, commissioning",
            "deliverables": "MEP design drawings, Fire safety report, Medical gas design, Staging plan, Commissioning procedures",
            "reference_documents": "AS 2896 Medical Gas, Healthcare guidelines, Fire safety codes, Electrical standards",
            "assumptions": "Staged construction possible, Temporary systems available, Specialized equipment procurement",
            "performance_requirements": "99.99% critical power reliability, Medical gas compliance, Fire safety compliance, Minimal disruption",
            "trust_score": 0.98,
            "days_old": 40
        },
        {
            "project_name": "Fremantle Port Automated Container Terminal",
            "project_number": "TKN-2024-AT-084",
            "program_region": "Western Australia",
            "category": "Port Automation",
            "project_leader": "Auto Port",
            "project_reviewer": "Robot Container",
            "lead_disciplines": "Automation, Electrical, Software, Mechanical",
            "client": "Fremantle Ports",
            "client_representative": "Digital Harbor",
            "background": "Convert existing container terminal to fully automated operation with automated guided vehicles and remote-controlled cranes.",
            "scope_of_work": "Design and implement automated container handling system including AGVs, automated cranes, and control systems.",
            "scope_of_services": "Automation design, control systems, software integration, safety systems, commissioning",
            "deliverables": "Automation specifications, Control software, Safety systems, Integration plan, Training program",
            "reference_documents": "Port automation standards, Safety regulations, Software standards, Equipment specifications",
            "assumptions": "Existing infrastructure suitable, Technology suppliers available, Staff training coordinated",
            "performance_requirements": "40 moves/hour/crane, 99.5% availability, Safety compliance, ROI targets",
            "trust_score": 0.89,
            "days_old": 110
        },
        {
            "project_name": "Blue Mountains Bushfire Early Warning System",
            "project_number": "TKN-2024-FW-095",
            "program_region": "New South Wales",
            "category": "Emergency Systems",
            "project_leader": "Fire Watch",
            "project_reviewer": "Early Warning",
            "lead_disciplines": "Electronics, Communications, Software, Environmental",
            "client": "NSW Rural Fire Service",
            "client_representative": "Chief Fire",
            "background": "Install comprehensive early warning system across 500km² of bushfire-prone area with cameras, sensors, and communication networks.",
            "scope_of_work": "Design and install network of fire detection cameras, weather stations, communication towers, and alert systems.",
            "scope_of_services": "System design, tower engineering, electronics design, software development, installation",
            "deliverables": "System architecture, Tower designs, Electronics specifications, Software documentation, Installation procedures",
            "reference_documents": "Emergency management standards, Communications regulations, Electronics standards, Environmental guidelines",
            "assumptions": "Site access available, Communication frequencies allocated, Power supply available",
            "performance_requirements": "5-minute detection time, 99% communication availability, Weather resistance, 15-year life",
            "trust_score": 0.92,
            "days_old": 65
        },
        {
            "project_name": "Tasmania Wind Farm Grid Connection",
            "project_number": "TKN-2024-WF-106",
            "program_region": "Tasmania",
            "category": "Renewable Energy",
            "project_leader": "Wind Power",
            "project_reviewer": "Grid Connect",
            "lead_disciplines": "Electrical, Environmental, Structural",
            "client": "TasNetworks",
            "client_representative": "Energy Grid",
            "background": "Connect 200MW wind farm to transmission grid via 50km 220kV transmission line through sensitive environmental areas.",
            "scope_of_work": "Design transmission line, substations, and grid connection infrastructure with minimal environmental impact.",
            "scope_of_services": "Transmission line design, substation design, environmental assessment, grid studies, construction planning",
            "deliverables": "Transmission line design, Substation design, Environmental approval, Grid connection study, Construction plan",
            "reference_documents": "AS 7000 Overhead Lines, Grid codes, Environmental regulations, Wind farm specifications",
            "assumptions": "Environmental approvals achievable, Grid capacity available, Access agreements obtained",
            "performance_requirements": "99.5% availability, Environmental compliance, Grid stability, 40-year design life",
            "trust_score": 0.90,
            "days_old": 95
        },
        {
            "project_name": "Sunshine Coast Smart City Infrastructure",
            "project_number": "TKN-2024-SC-117",
            "program_region": "Queensland",
            "category": "Smart City",
            "project_leader": "Smart Tech",
            "project_reviewer": "Digital City",
            "lead_disciplines": "ICT, Urban Planning, Electronics",
            "client": "Sunshine Coast Council",
            "client_representative": "Innovation Manager",
            "background": "Implement smart city infrastructure including IoT sensors, smart lighting, traffic management, and digital services platform.",
            "scope_of_work": "Deploy smart city technologies across 25km² urban area including sensors, communications, data analytics, and citizen services.",
            "scope_of_services": "Technology architecture, sensor network design, data platform development, integration services",
            "deliverables": "Technology specifications, Network design, Data platform, Integration plan, User interfaces",
            "reference_documents": "Smart city standards, ICT guidelines, Privacy regulations, Security standards",
            "assumptions": "Telecommunications infrastructure adequate, Data privacy compliance, Technology procurement available",
            "performance_requirements": "Real-time data processing, 99% network availability, Privacy compliance, Scalable architecture",
            "trust_score": 0.84,
            "days_old": 120
        },
        {
            "project_name": "Alice Springs Solar Farm and Storage",
            "project_number": "TKN-2024-SF-128",
            "program_region": "Northern Territory",
            "category": "Solar Energy",
            "project_leader": "Solar Power",
            "project_reviewer": "Battery Storage",
            "lead_disciplines": "Electrical, Environmental, Civil",
            "client": "Territory Generation",
            "client_representative": "Renewable Manager",
            "background": "100MW solar farm with 50MWh battery storage to provide renewable energy for remote mining operations and grid stability.",
            "scope_of_work": "Design solar PV array, battery energy storage system, grid connection, and control systems for remote operation.",
            "scope_of_services": "Solar design, battery system design, electrical infrastructure, control systems, environmental assessment",
            "deliverables": "Solar farm design, Battery specifications, Electrical design, Control systems, Environmental approval",
            "reference_documents": "AS 4777 Grid Connection, Battery standards, Solar standards, Environmental guidelines",
            "assumptions": "Grid connection capacity available, Land tenure secured, Equipment procurement coordinated",
            "performance_requirements": "25% capacity factor, 4-hour storage duration, Remote operation capability, 25-year life",
            "trust_score": 0.88,
            "days_old": 80
        },
        {
            "project_name": "Wollongong Steel Works Water Recycling",
            "project_number": "TKN-2023-WR-139",
            "program_region": "New South Wales",
            "category": "Industrial Water",
            "project_leader": "Industrial Water",
            "project_reviewer": "Process Expert",
            "lead_disciplines": "Chemical Engineering, Process, Environmental",
            "client": "BlueScope Steel",
            "client_representative": "Plant Manager",
            "background": "Design water recycling system to reduce freshwater consumption by 80% and eliminate industrial discharge to ocean.",
            "scope_of_work": "Design integrated water treatment and recycling system for steel manufacturing processes including cooling water and process water recovery.",
            "scope_of_services": "Process design, treatment technology selection, system integration, environmental assessment, commissioning",
            "deliverables": "Process design package, Treatment specifications, System integration plan, Environmental compliance, Operating procedures",
            "reference_documents": "Industrial water standards, Steel industry guidelines, Environmental regulations, Process specifications",
            "assumptions": "Existing infrastructure suitable, Chemical supply available, Environmental approvals achievable",
            "performance_requirements": "80% water reduction, Zero liquid discharge, Process water quality standards, Economic viability",
            "trust_score": 0.95,
            "days_old": 150
        },
        {
            "project_name": "Geelong Manufacturing Precinct Infrastructure",
            "project_number": "TKN-2024-MP-150",
            "program_region": "Victoria",
            "category": "Industrial Infrastructure",
            "project_leader": "Industry Build",
            "project_reviewer": "Manufacturing Expert",
            "lead_disciplines": "Civil, Electrical, Environmental, Transport",
            "client": "Development Victoria",
            "client_representative": "Precinct Director",
            "background": "Design infrastructure for 500-hectare advanced manufacturing precinct including roads, utilities, rail siding, and digital infrastructure.",
            "scope_of_work": "Design complete infrastructure package for industrial precinct including transport, utilities, telecommunications, and environmental systems.",
            "scope_of_services": "Master planning, infrastructure design, utility design, transport planning, environmental assessment",
            "deliverables": "Master plan, Infrastructure designs, Utility plans, Transport strategy, Environmental management",
            "reference_documents": "Industrial development standards, Planning regulations, Utility standards, Transport guidelines",
            "assumptions": "Planning approvals achievable, Utility connections available, Transport access coordinated",
            "performance_requirements": "Heavy vehicle access, High-speed internet, Reliable utilities, Environmental sustainability",
            "trust_score": 0.87,
            "days_old": 55
        }
    ]
    
    # Store in database
    db = KnowledgeDatabase()
    
    print("🔄 Creating 20 diverse project documents...")
    
    for i, project in enumerate(projects, 1):
        # Add timestamps based on days_old
        now = datetime.now()
        days_ago = project.pop('days_old', random.randint(30, 200))
        project['created_date'] = (now - timedelta(days=days_ago + 10)).isoformat()
        project['modified_date'] = (now - timedelta(days=days_ago)).isoformat()
        
        # Add file metadata
        project['file_path'] = f"data/sample_{project['project_number'].lower().replace('-', '_')}.docx"
        project['file_name'] = f"{project['project_name'].replace(' ', '_')}_PBR.docx"
        project['file_size'] = random.randint(150000, 400000)
        
        # Add trust badges based on score and content
        badges = []
        if project.get('project_reviewer'):
            badges.append('Has Reviewer')
        if project.get('project_name') and project.get('client'):
            badges.append('Complete Header')
        if project.get('background') and project.get('scope_of_work'):
            badges.append('Complete Content')
        if project.get('program_region'):
            badges.append('Region Specified')
        if project['trust_score'] >= 0.9:
            badges.append('High Quality')
        if project.get('reference_documents'):
            badges.append('References Cited')
        
        project['trust_badges'] = badges
        
        # Create comprehensive searchable text
        searchable_parts = []
        for field in ['project_name', 'category', 'program_region', 'lead_disciplines', 
                     'client', 'background', 'scope_of_work', 'scope_of_services', 
                     'deliverables', 'assumptions', 'performance_requirements']:
            if project.get(field):
                searchable_parts.append(str(project[field]))
        
        project['searchable_text'] = ' '.join(searchable_parts)
        
        # Store in database
        doc_id = db.store_document(project)
        print(f"✅ {i:2d}. {project['project_name'][:50]:<50} | {project['program_region']:<20} | Score: {project['trust_score']}")
    
    print(f"\n🎉 Created {len(projects)} diverse project documents!")
    
    # Show comprehensive stats
    stats = db.get_stats()
    print(f"\n📊 Database Summary:")
    print(f"   • Total Documents: {stats['total_documents']}")
    print(f"   • Average Trust Score: {stats['avg_trust_score']:.2f}")
    
    # Show breakdown by region
    all_docs = db.get_all_documents()
    regions = {}
    categories = {}
    for doc in all_docs:
        region = doc.get('program_region', 'Unknown')
        category = doc.get('category', 'Unknown')
        regions[region] = regions.get(region, 0) + 1
        categories[category] = categories.get(category, 0) + 1
    
    print(f"\n🌏 By Region:")
    for region, count in sorted(regions.items()):
        print(f"   • {region}: {count} projects")
    
    print(f"\n🏗️ By Category:")
    for category, count in sorted(categories.items()):
        print(f"   • {category}: {count} projects")
    
    return len(projects)

def main():
    """Main function."""
    print("🚀 Tonkin Knowledge Finder - Expanded Data Creator")
    print("=" * 60)
    
    # Clear existing data
    db = KnowledgeDatabase()
    print("🗑️ Clearing existing sample data...")
    
    count = create_expanded_projects()
    
    print(f"\n✅ Enhanced dataset created successfully!")
    print(f"\n📋 Next steps:")
    print("1. Run: python -c \"import sys; sys.path.append('src'); from search import SemanticSearchEngine; SemanticSearchEngine().create_embeddings_for_documents(force_rebuild=True)\"")
    print("2. Start app: streamlit run app.py")
    print("\n🔍 Try searching for:")
    print("   • 'stormwater management SA'")
    print("   • 'bridge design NSW'") 
    print("   • 'renewable energy projects'")
    print("   • 'water treatment plants'")
    print("   • 'Melbourne metro projects'")
    print("   • 'high quality infrastructure'")
    print("   • 'coastal protection works'")
    print("   • 'smart city technology'")

if __name__ == "__main__":
    main()
