// Sample data for testing and demo purposes
export const sampleProjects = [
  {
    id: 1,
    projectNumber: "TKN-2024-MP-150",
    projectName: "Melbourne Port Infrastructure Upgrade",
    description: "Major upgrade to port facilities including new container terminal and improved logistics infrastructure",
    client: "Development Victoria",
    region: "Victoria",
    category: "Industrial Infrastructure",
    projectType: "Infrastructure Development",
    phase: "Design Complete",
    startDate: "2024-01-15",
    completionDate: "2024-12-20",
    trustScore: 0.87,
    similarityScore: 0.94,
    projectLeader: "Sarah Mitchell",
    projectReviewer: "David Chen",
    disciplines: ["Civil", "Electrical", "Environmental", "Transport"],
    budget: "$45M",
    status: "Active",
    riskLevel: "Medium",
    lessons: [
      {
        id: 1,
        text: "Early stakeholder engagement crucial for port projects",
        author: "Sarah Mitchell",
        date: "2024-03-10",
        phase: "Planning"
      }
    ],
    tags: ["port", "logistics", "container terminal", "infrastructure"]
  },
  {
    id: 2,
    projectNumber: "TKN-2024-SW-089",
    projectName: "Sydney Waterfront Stormwater Management System",
    description: "Comprehensive stormwater detention and treatment system for coastal development",
    client: "Sydney Water Corporation",
    region: "New South Wales",
    category: "Water Infrastructure",
    projectType: "Stormwater Management",
    phase: "Construction",
    startDate: "2024-02-01",
    completionDate: "2025-06-30",
    trustScore: 0.92,
    similarityScore: 0.89,
    projectLeader: "James Wilson",
    projectReviewer: "Sarah Mitchell",
    disciplines: ["Civil", "Hydraulic", "Environmental"],
    budget: "$12M",
    status: "Active",
    riskLevel: "Low",
    lessons: [
      {
        id: 2,
        text: "Integration with existing systems requires detailed coordination",
        author: "James Wilson",
        date: "2024-04-15",
        phase: "Design"
      }
    ],
    tags: ["stormwater", "detention", "coastal", "water treatment"]
  },
  {
    id: 3,
    projectNumber: "TKN-2023-BR-045",
    projectName: "Brisbane Gateway Bridge Expansion",
    description: "Bridge widening and structural strengthening project to increase traffic capacity",
    client: "Queensland Department of Transport",
    region: "Queensland",
    category: "Transport Infrastructure",
    projectType: "Bridge Engineering",
    phase: "Completed",
    startDate: "2023-06-10",
    completionDate: "2024-03-25",
    trustScore: 0.95,
    similarityScore: 0.78,
    projectLeader: "Emma Thompson",
    projectReviewer: "David Chen",
    disciplines: ["Structural", "Civil", "Traffic Engineering", "Geotechnical"],
    budget: "$28M",
    status: "Completed",
    riskLevel: "High",
    lessons: [
      {
        id: 3,
        text: "Traffic management during construction is critical for public acceptance",
        author: "Emma Thompson",
        date: "2023-09-20",
        phase: "Construction"
      },
      {
        id: 4,
        text: "Weather-dependent activities need significant buffer time",
        author: "David Chen",
        date: "2023-11-05",
        phase: "Construction"
      }
    ],
    tags: ["bridge", "structural", "expansion", "traffic"]
  },
  {
    id: 4,
    projectNumber: "TKN-2024-EN-112",
    projectName: "Adelaide Renewable Energy Hub",
    description: "Solar farm and battery storage facility for commercial and industrial users",
    client: "SA Power Networks",
    region: "South Australia",
    category: "Energy Infrastructure",
    projectType: "Renewable Energy",
    phase: "Feasibility",
    startDate: "2024-04-01",
    completionDate: "2025-12-31",
    trustScore: 0.78,
    similarityScore: 0.85,
    projectLeader: "Michael O'Brien",
    projectReviewer: "Emma Thompson",
    disciplines: ["Electrical", "Environmental", "Civil"],
    budget: "$65M",
    status: "Planning",
    riskLevel: "Medium",
    lessons: [],
    tags: ["solar", "renewable", "battery storage", "energy"]
  },
  {
    id: 5,
    projectNumber: "TKN-2024-WT-078",
    projectName: "Perth Water Treatment Facility Modernization",
    description: "Upgrade of existing water treatment plant with advanced filtration technology",
    client: "Water Corporation WA",
    region: "Western Australia",
    category: "Water Infrastructure",
    projectType: "Treatment Plant",
    phase: "Design",
    startDate: "2024-03-15",
    completionDate: "2025-09-30",
    trustScore: 0.89,
    similarityScore: 0.82,
    projectLeader: "Lisa Anderson",
    projectReviewer: "James Wilson",
    disciplines: ["Chemical", "Civil", "Mechanical", "Process Engineering"],
    budget: "$32M",
    status: "Active",
    riskLevel: "Medium",
    lessons: [
      {
        id: 5,
        text: "Phased implementation allows continuous operation during upgrade",
        author: "Lisa Anderson",
        date: "2024-05-20",
        phase: "Design"
      }
    ],
    tags: ["water treatment", "filtration", "modernization", "process"]
  },
  {
    id: 6,
    projectNumber: "TKN-2023-SC-033",
    projectName: "Melbourne Smart City IoT Network",
    description: "City-wide sensor network for traffic, environmental, and infrastructure monitoring",
    client: "City of Melbourne",
    region: "Victoria",
    category: "Smart Infrastructure",
    projectType: "IoT Systems",
    phase: "Implementation",
    startDate: "2023-11-01",
    completionDate: "2024-10-31",
    trustScore: 0.83,
    similarityScore: 0.76,
    projectLeader: "David Chen",
    projectReviewer: "Michael O'Brien",
    disciplines: ["Electrical", "Data Science", "Civil", "IT"],
    budget: "$18M",
    status: "Active",
    riskLevel: "Low",
    lessons: [
      {
        id: 6,
        text: "Data security and privacy must be designed in from the start",
        author: "David Chen",
        date: "2024-01-12",
        phase: "Design"
      }
    ],
    tags: ["smart city", "IoT", "sensors", "monitoring"]
  }
];

export const expertProfiles = [
  {
    name: "Sarah Mitchell",
    role: "Senior Infrastructure Lead",
    email: "sarah.mitchell@tonkin.com.au",
    slack: "@smitchell",
    expertise: ["Industrial Infrastructure", "Port Engineering", "Project Management"],
    projectsLed: 12,
    projectsReviewed: 28,
    avgTrustScore: 0.91,
    recentProjects: ["TKN-2024-MP-150", "TKN-2024-SW-089"],
    avatar: "SM"
  },
  {
    name: "David Chen",
    role: "Bridge & Structural Expert",
    email: "david.chen@tonkin.com.au",
    slack: "@dchen",
    expertise: ["Structural Engineering", "Bridge Design", "Smart Infrastructure"],
    projectsLed: 8,
    projectsReviewed: 34,
    avgTrustScore: 0.93,
    recentProjects: ["TKN-2023-BR-045", "TKN-2023-SC-033"],
    avatar: "DC"
  },
  {
    name: "James Wilson",
    role: "Water Infrastructure Specialist",
    email: "james.wilson@tonkin.com.au",
    slack: "@jwilson",
    expertise: ["Stormwater Management", "Hydraulic Engineering", "Water Treatment"],
    projectsLed: 15,
    projectsReviewed: 22,
    avgTrustScore: 0.88,
    recentProjects: ["TKN-2024-SW-089", "TKN-2024-WT-078"],
    avatar: "JW"
  },
  {
    name: "Emma Thompson",
    role: "Transport & Bridge Lead",
    email: "emma.thompson@tonkin.com.au",
    slack: "@ethompson",
    expertise: ["Bridge Engineering", "Traffic Engineering", "Structural Analysis"],
    projectsLed: 10,
    projectsReviewed: 19,
    avgTrustScore: 0.94,
    recentProjects: ["TKN-2023-BR-045", "TKN-2024-EN-112"],
    avatar: "ET"
  },
  {
    name: "Michael O'Brien",
    role: "Renewable Energy Expert",
    email: "michael.obrien@tonkin.com.au",
    slack: "@mobrien",
    expertise: ["Renewable Energy", "Electrical Systems", "Battery Storage"],
    projectsLed: 7,
    projectsReviewed: 15,
    avgTrustScore: 0.86,
    recentProjects: ["TKN-2024-EN-112", "TKN-2023-SC-033"],
    avatar: "MO"
  },
  {
    name: "Lisa Anderson",
    role: "Process Engineering Lead",
    email: "lisa.anderson@tonkin.com.au",
    slack: "@landerson",
    expertise: ["Water Treatment", "Chemical Engineering", "Process Design"],
    projectsLed: 11,
    projectsReviewed: 25,
    avgTrustScore: 0.90,
    recentProjects: ["TKN-2024-WT-078"],
    avatar: "LA"
  }
];

export const categories = [
  "Industrial Infrastructure",
  "Water Infrastructure",
  "Transport Infrastructure",
  "Energy Infrastructure",
  "Smart Infrastructure",
  "Building Services"
];

export const regions = [
  "Victoria",
  "New South Wales",
  "Queensland",
  "South Australia",
  "Western Australia",
  "Tasmania",
  "Northern Territory",
  "Australian Capital Territory"
];

