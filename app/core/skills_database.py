"""
Comprehensive skills dictionary and action verbs database for AI Resume Analyser.
Categorized into programming languages, frameworks, cloud/devops, databases,
AI/Data, soft skills, and industry standard keywords.
"""

SKILLS_TAXONOMY = {
    "Programming Languages": [
        "python", "javascript", "typescript", "java", "c++", "c#", "c", "go", "golang",
        "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "dart", "shell", "bash",
        "powershell", "perl", "haskell", "lua", "matlab", "julia", "sql", "html", "html5",
        "css", "css3", "sass", "scss", "solidity"
    ],
    "Frameworks & Libraries": [
        "react", "react.js", "next.js", "vue", "vue.js", "nuxt.js", "angular", "svelte",
        "node.js", "express", "express.js", "django", "flask", "fastapi", "spring", "spring boot",
        ".net", "asp.net", "ruby on rails", "laravel", "pytorch", "tensorflow", "keras",
        "scikit-learn", "sklearn", "pandas", "numpy", "scipy", "opencv", "matplotlib",
        "seaborn", "tailwind", "tailwind css", "bootstrap", "material ui", "chakra ui",
        "redux", "zustand", "graphql", "apollo", "rest api", "grpc", "jest", "pytest",
        "cypress", "selenium", "playwright", "langchain", "llamaindex", "hugging face"
    ],
    "Cloud, DevOps & Infrastructure": [
        "aws", "amazon web services", "azure", "microsoft azure", "gcp", "google cloud platform",
        "docker", "kubernetes", "k8s", "terraform", "ansible", "jenkins", "github actions",
        "gitlab ci", "ci/cd", "continuous integration", "helm", "linux", "ubuntu", "nginx",
        "apache", "serverless", "aws lambda", "cloudformation", "prometheus", "grafana",
        "datadog", "elk stack", "splunk", "openshift", "circleci", "argo cd"
    ],
    "Databases & Storage": [
        "postgresql", "postgres", "mysql", "sqlite", "mongodb", "redis", "elasticsearch",
        "cassandra", "dynamodb", "mariadb", "oracle db", "sql server", "mssql", "neo4j",
        "couchdb", "firebase", "supabase", "snowflake", "bigquery", "redshift", "pinecone",
        "weaviate", "chromadb", "qdrant", "milvus"
    ],
    "AI, ML & Data Engineering": [
        "machine learning", "deep learning", "artificial intelligence", "data science",
        "nlp", "natural language processing", "computer vision", "llm", "large language models",
        "generative ai", "genai", "prompt engineering", "rag", "retrieval-augmented generation",
        "fine-tuning", "bert", "gpt", "transformers", "data analysis", "data engineering",
        "etl", "elt", "apache spark", "spark", "apache kafka", "kafka", "hadoop", "airflow",
        "dbt", "databricks", "mlops", "tableau", "power bi", "looker", "reinforcement learning"
    ],
    "Software Engineering & Architecture": [
        "microservices", "system design", "object-oriented programming", "oop", "functional programming",
        "mvc", "design patterns", "test-driven development", "tdd", "clean architecture",
        "api design", "restful", "distributed systems", "event-driven architecture", "caching",
        "web security", "oauth", "jwt", "saml", "cryptography", "version control", "git",
        "code review", "debugging", "profiling", "performance optimization"
    ],
    "Product & Project Management": [
        "agile", "scrum", "kanban", "jira", "confluence", "trello", "asana", "product roadmap",
        "user stories", "sprint planning", "stakeholder management", "kpi tracking", "a/b testing",
        "wireframing", "figma", "ui/ux design", "market research", "customer journey"
    ],
    "Soft Skills & Leadership": [
        "leadership", "communication", "team collaboration", "problem solving", "critical thinking",
        "mentorship", "adaptability", "time management", "conflict resolution", "cross-functional collaboration",
        "decision making", "presentation skills", "negotiation", "ownership", "analytical thinking"
    ]
}

# Flattened set of all known skills (lower-cased for rapid O(1) lookup)
ALL_SKILLS_SET = {
    skill.lower()
    for category, skills in SKILLS_TAXONOMY.items()
    for skill in skills
}

# Strong action verbs favored by top ATS systems
ACTION_VERBS = {
    "leadership": [
        "spearheaded", "orchestrated", "championed", "directed", "founded", "headed",
        "guided", "mentored", "mobilized", "supervised", "governed", "cultivated"
    ],
    "creation_and_engineering": [
        "architected", "engineered", "developed", "designed", "built", "implemented",
        "authored", "constructed", "devised", "formulated", "pioneered", "fashioned"
    ],
    "optimization_and_growth": [
        "optimized", "streamlined", "accelerated", "scaled", "boosted", "amplified",
        "reduced", "eliminated", "automated", "transformed", "revamped", "modernized",
        "enhanced", "maximized", "minimized", "consolidated"
    ],
    "delivery_and_execution": [
        "delivered", "deployed", "executed", "launched", "published", "dispatched",
        "negotiated", "resolved", "secured", "integrated", "maintained", "migrated"
    ],
    "analysis_and_research": [
        "analyzed", "assessed", "audited", "benchmarked", "evaluated", "diagnosed",
        "investigated", "quantified", "synthesized", "identified", "mapped"
    ]
}

ALL_ACTION_VERBS = {
    verb
    for category, verbs in ACTION_VERBS.items()
    for verb in verbs
}

# Weak, passive, or cliché words that lower ATS impact
WEAK_WORDS = [
    "responsible for", "duties included", "helped with", "assisted in", "worked on",
    "participated in", "attempted", "hard worker", "team player", "go-getter",
    "think outside the box", "synergy", "self-motivated", "detail-oriented"
]
