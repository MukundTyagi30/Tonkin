#!/usr/bin/env python3
"""Create sample SF84 documents with realistic project data for testing."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from database import KnowledgeDatabase
from parser import SF84Document
from datetime import datetime, timedelta

def create_sample_documents():
    """Create sample project documents for testing."""
    
    # Sample project data based on typical Tonkin projects
    sample_projects = [
        {
            "file_path": "data/sample_stormwater_detention_sa.json",
            "file_name": "Stormwater_Detention_Project_SA_PBR.docx",
            "file_size": 250000,
            "project_name": "Adelaide Hills Stormwater Detention Basin",
            "project_number": "TKN-2024-SW-001",
            "program_region": "South Australia",
            "category": "Stormwater Management",
            "project_leader": "Sarah Mitchell",
            "project_reviewer": "David Chen",
            "lead_disciplines": "Hydraulic Engineering, Environmental",
            "client": "Adelaide Hills Council",
            "client_representative": "Mark Thompson",
            "background": "The Adelaide Hills Council requires a new detention basin to manage stormwater runoff from the expanding residential development in the Mount Barker area. Current infrastructure is inadequate for the increased flow volumes.",
            "scope_of_work": "Design and construct a 50,000m³ detention basin with inlet/outlet structures, landscaping, and environmental controls. Include flood modeling and environmental impact assessment.",
            "scope_of_services": "Hydraulic modeling, detailed design, environmental assessment, construction documentation, construction supervision, and commissioning support.",
            "deliverables": "Hydraulic model report, Design drawings (civil, structural, electrical), Environmental management plan, Construction specifications, As-built documentation",
            "reference_documents": "Australian Rainfall & Runoff Guidelines 2019, SA Planning Code, Council Development Standards, Flood mapping data from DEW",
            "assumptions": "Site access available during construction, No contaminated materials expected, Standard soil conditions per geotechnical report",
            "performance_requirements": "1:100 year ARI flood protection, Environmental flow releases, Maximum 2m/s outlet velocity, Native vegetation retention >80%",
            "trust_score": 0.95
        },
        {
            "file_path": "data/sample_bridge_design_nsw.json", 
            "file_name": "Pacific_Highway_Bridge_Design_PBR.docx",
            "file_size": 180000,
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
            "trust_score": 0.88
        },
        {
            "file_path": "data/sample_water_treatment_wa.json",
            "file_name": "Perth_WTP_Upgrade_PBR.docx", 
            "file_size": 320000,
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
            "trust_score": 0.92
        }
    ]
    
    # Store in database
    db = KnowledgeDatabase()
    
    print("🔄 Creating sample project documents...")
    
    for i, project in enumerate(sample_projects, 1):
        # Add timestamps
        now = datetime.now()
        project['created_date'] = (now - timedelta(days=30*i)).isoformat()
        project['modified_date'] = (now - timedelta(days=10*i)).isoformat()
        
        # Add trust badges based on score
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
        
        project['trust_badges'] = badges
        
        # Create searchable text
        searchable_parts = []
        for field in ['project_name', 'background', 'scope_of_work', 'scope_of_services', 
                     'deliverables', 'assumptions', 'performance_requirements']:
            if project.get(field):
                searchable_parts.append(project[field])
        
        project['searchable_text'] = ' '.join(searchable_parts)
        
        # Store in database
        doc_id = db.store_document(project)
        print(f"✅ Created: {project['project_name']} (ID: {doc_id})")
    
    print(f"\n🎉 Created {len(sample_projects)} sample documents!")
    
    # Show stats
    stats = db.get_stats()
    print(f"📊 Database stats: {stats}")
    
    return len(sample_projects)

def main():
    """Main function."""
    print("🚀 Tonkin Knowledge Finder - Sample Data Creator")
    print("=" * 50)
    
    count = create_sample_documents()
    
    print(f"\n✅ Sample data created successfully!")
    print(f"\n📋 Next steps:")
    print("1. Run: python ingest/create_index.py --skip-indexing  # Create embeddings")
    print("2. Start app: streamlit run app.py")
    print("\n💡 Try searching for:")
    print("   - 'stormwater detention SA'")
    print("   - 'bridge design NSW'") 
    print("   - 'water treatment Perth'")
    print("   - 'projects by Sarah Mitchell'")
    print("   - 'high quality approved projects'")

if __name__ == "__main__":
    main()
