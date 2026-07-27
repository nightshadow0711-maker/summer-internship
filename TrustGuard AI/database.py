import sqlite3
from datetime import datetime
from config.settings import DATABASE_PATH

def get_connection():
    # Added check_same_thread=False for Streamlit compatibility
    conn = sqlite3.connect(str(DATABASE_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS analyses (
        analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_title TEXT,
        article_text TEXT NOT NULL,
        article_url TEXT,
        input_type TEXT,
        ml_prediction TEXT,
        real_probability REAL,
        fake_probability REAL,
        ml_confidence REAL,
        online_status TEXT,
        supporting_sources INTEGER DEFAULT 0,
        conflicting_sources INTEGER DEFAULT 0,
        neutral_sources INTEGER DEFAULT 0,
        fact_check_status TEXT,
        source_credibility REAL,
        final_score REAL,
        final_assessment TEXT,
        verification_note TEXT,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS evidence (
        evidence_id INTEGER PRIMARY KEY AUTOINCREMENT,
        analysis_id INTEGER,
        source_name TEXT,
        title TEXT,
        url TEXT,
        evidence_type TEXT,
        relevance REAL,
        credibility REAL,
        published_at TEXT,
        FOREIGN KEY(analysis_id) REFERENCES analyses(analysis_id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS fact_checks (
        fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
        analysis_id INTEGER,
        publisher TEXT,
        claim TEXT,
        rating TEXT,
        url TEXT,
        FOREIGN KEY(analysis_id) REFERENCES analyses(analysis_id) ON DELETE CASCADE
    );
    """)
    conn.commit()
    conn.close()

def save_analysis(result, article_text="", source_name="", article_url="", input_type="text"):
    """
    Saves the nested verification pipeline result into the flat database schema.
    """
    init_db()  # Safety check: ensure tables exist before saving
    conn = get_connection()
    
    # Flatten the nested result dictionaries
    ml = result.get("ml", {})
    online = result.get("online", {})
    fact_check = result.get("fact_check", {})
    source_res = result.get("source", {})
    final = result.get("final", {})

    # Generate title from the first sentence if not provided
    clean_lines = [line.strip() for line in article_text.splitlines() if line.strip()]
    article_title = clean_lines[0][:100] if clean_lines else "Untitled Analysis"
    
    # Calculate source counts
    sources = online.get("sources", [])
    supporting_count = sum(1 for s in sources if s.get("evidence_type") == "supporting")
    conflicting_count = sum(1 for s in sources if s.get("evidence_type") == "conflicting")
    neutral_count = len(sources) - supporting_count - conflicting_count

    cur = conn.execute("""
    INSERT INTO analyses (
      article_title, article_text, article_url, input_type, ml_prediction,
      real_probability, fake_probability, ml_confidence, online_status,
      supporting_sources, conflicting_sources, neutral_sources, fact_check_status,
      source_credibility, final_score, final_assessment, verification_note, created_at
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        article_title, 
        article_text, 
        article_url, 
        input_type, 
        ml.get("prediction", "UNCERTAIN"), 
        float(ml.get("real_probability", 50.0)),
        float(ml.get("fake_probability", 50.0)), 
        float(ml.get("confidence", 0.0)), 
        online.get("status", "NOT_FOUND"),
        supporting_count, 
        conflicting_count, 
        neutral_count, 
        fact_check.get("status", "NOT_FOUND"), 
        float(source_res.get("score", 50.0)), 
        float(final.get("score", 50.0)),
        final.get("verdict", "UNCERTAIN"), 
        f"Verdict: {final.get('verdict', 'UNCERTAIN')} | Score: {final.get('score', 50)}/100",
        datetime.now().isoformat(timespec="seconds")
    ))
    
    analysis_id = cur.lastrowid
    
    # Insert Online News Evidence
    for s in sources:
        conn.execute("""INSERT INTO evidence
        (analysis_id,source_name,title,url,evidence_type,relevance,credibility,published_at)
        VALUES (?,?,?,?,?,?,?,?)""", (
            analysis_id, 
            s.get("source_name", s.get("source", "Unknown")), 
            s.get("title", ""),
            s.get("url", ""), 
            s.get("evidence_type", "neutral"),
            float(s.get("relevance", 0.0)), 
            float(s.get("credibility", 0.0)), 
            s.get("published_at", "")
        ))
        
    # Insert Fact Check Evidence
    for f in fact_check.get("claims", []):
        conn.execute("""INSERT INTO fact_checks
        (analysis_id,publisher,claim,rating,url) VALUES (?,?,?,?,?)""", (
            analysis_id, 
            f.get("publisher", ""), 
            f.get("claim", ""),
            f.get("rating", ""), 
            f.get("url", "")
        ))
        
    conn.commit()
    conn.close()
    return analysis_id

def list_analyses(limit=500):
    init_db() # Prevent "no such table" error if reading before writing
    conn = get_connection()
    rows = conn.execute("SELECT * FROM analyses ORDER BY analysis_id DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_analysis(analysis_id):
    init_db()
    conn = get_connection()
    row = conn.execute("SELECT * FROM analyses WHERE analysis_id=?", (analysis_id,)).fetchone()
    sources = conn.execute("SELECT * FROM evidence WHERE analysis_id=?", (analysis_id,)).fetchall()
    facts = conn.execute("SELECT * FROM fact_checks WHERE analysis_id=?", (analysis_id,)).fetchall()
    conn.close()
    
    if not row:
        return None
        
    result = dict(row)
    result["sources"] = [dict(x) for x in sources]
    result["fact_checks"] = [dict(x) for x in facts]
    return result

def delete_analysis(analysis_id):
    init_db()
    conn = get_connection()
    conn.execute("DELETE FROM evidence WHERE analysis_id=?", (analysis_id,))
    conn.execute("DELETE FROM fact_checks WHERE analysis_id=?", (analysis_id,))
    conn.execute("DELETE FROM analyses WHERE analysis_id=?", (analysis_id,))
    conn.commit()
    conn.close()