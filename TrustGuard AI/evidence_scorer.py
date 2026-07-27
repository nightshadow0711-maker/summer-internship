def assess_evidence(sources):
    if not sources:
        return {"supporting":0,"conflicting":0,"neutral":0,"score":50.0,"status":"UNAVAILABLE"}
    supporting=sum(1 for s in sources if s.get("evidence_type")=="supporting")
    conflicting=sum(1 for s in sources if s.get("evidence_type")=="conflicting")
    neutral=len(sources)-supporting-conflicting
    score=sum(float(s.get("credibility",50))*float(s.get("relevance",50))/100 for s in sources)/len(sources)
    if supporting and conflicting:
        status="MIXED"
    elif supporting:
        status="SUPPORTED"
    else:
        status="NEUTRAL"
    return {"supporting":supporting,"conflicting":conflicting,"neutral":neutral,"score":round(score,1),"status":status}

def final_assessment(ml, evidence, fact_status, has_external_config=False):
    ml_score=float(ml["real_probability"])
    ev_score=float(evidence["score"])
    if fact_status=="FALSE": fact_score=10
    elif fact_status=="SUPPORTED": fact_score=90
    elif fact_status=="DISPUTED": fact_score=35
    elif fact_status=="NO_MATCH": fact_score=50
    else: fact_score=50
    source_score=ev_score

    # ML score is a "real" probability. Evidence/fact-check are independent signals.
    final=(ml_score*0.40)+(ev_score*0.25)+(fact_score*0.20)+(source_score*0.15)
    if fact_status=="FALSE" or evidence["conflicting"]>evidence["supporting"]:
        final=min(final,49)
    if final>=80: label="LIKELY REAL"
    elif final>=60: label="REAL"
    elif final>=40: label="UNCERTAIN"
    elif final>=20: label="LIKELY FAKE"
    else: label="FAKE"
    note="Final score combines model prediction and available evidence. "
    if not has_external_config:
        note += "Online API credentials are not configured; external verification may be limited."
    return round(final,1), label, note
