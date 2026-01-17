import random
from datetime import date
import json
import os

# Expanded emotional and inclusive vocabulary
concern_symptoms = [
    "pain", "itching", "rashes", "bumps", "unusual discharge", "bleeding", "cramps", "nausea", "dizziness", "headaches",
    "soreness", "burning sensation", "missed period", "unexpected spotting", "fatigue", "tender breasts"
]

concern_actions = [
    "having unprotected sex", "missing a pill", "using emergency contraception", "not using a condom",
    "switching birth control", "taking antibiotics", "sharing a towel", "using public restrooms", 
    "touching myself down there", "having oral sex", "not pulling out in time"
]

emotional_phrases = [
    "I'm freaking out", "I'm panicking", "I feel really anxious", "I'm losing sleep over this",
    "I'm so embarrassed", "I can't stop worrying", "I'm terrified", "I feel hopeless", "I need help fast", 
    "I feel ashamed", "I feel guilty", "I'm afraid my parents will find out", "I'm scared to talk to anyone"
]

inclusive_partner_phrases = [
    "My partner (they/them)", "My partner (she/her)", "My partner (he/him)", "My significant other"
]

concern_events = [
    "I missed my birth control pill",
    "the condom broke",
    "my partner finished inside me",
    "I had unprotected sex",
    "I think my period is late",
    "there was blood after sex",
    "I feel a burning sensation",
    "my partner pressured me",
    "my parents can't know about this"
]

concern_templates = [
    "{emotional} because {event}. What should I do?",
    "Help! {event} and now I'm {emotional}.",
    "{symptom} after {event}, should I be concerned?",
    "I feel {emotional} after {action}, am I okay?",
    "Missed my contraception and now I'm {emotional}, please help!",
    "Is it dangerous if {situation}? {emotional}.",
    "{partner} says {claim}, and now I'm {emotional}. Is that true?",
    "I had unprotected sex and now have {symptom}—could it be serious?",
    "I feel {emotional} because my partner (they/them) {event}. Is everything okay?",
    "This is so embarrassing and scary—{symptom} after {event}."
]

belief_templates = [
    "{claim}. Is that true?",
    "I've heard that {claim}. Is it correct?",
    "{claim}, right?",
    "People say {claim}, but I’m not sure.",
    "Is it a fact that {claim}?",
    "My friend told me that {claim}. Should I believe them?",
    "Someone at school says {claim}; is that accurate?"
]

belief_claims = [
    "You can't get pregnant your first time",
    "STIs always show symptoms",
    "Pulling out is completely safe",
    "Condoms never fail",
    "Birth control makes you infertile",
    "You can't get pregnant during your period",
    "Double condoms provide double protection",
    "HPV always causes cancer",
    "Peeing after sex stops pregnancy",
    "You can't get an STI from oral sex",
    "If there's no symptoms, there's no STI",
    "Taking a shower after sex prevents pregnancy",
    "Pre-cum can't cause pregnancy",
    "You can't get pregnant standing up"
]

needs_verification_templates = [
    "Is it true that {claim}?",
    "Can you confirm if {claim}?",
    "Should I believe '{claim}'?",
    "Does it check out that {claim}?",
    "Fact check: {claim}",
    "Please clarify: {claim}",
    "Is this accurate: '{claim}'?",
    "Not sure if this is real: {claim}. Can you help?"
]

def prompt_user(sample):
    print("\nGenerated query:")
    print(json.dumps(sample, indent=2, ensure_ascii=False))
    resp = input("Add this query to the file? (y/n/q to quit): ").strip().lower()
    return resp

def append_to_file(sample, filename):
    # Append as a JSON line (or collect and write as a list if you prefer)
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(sample, ensure_ascii=False) + "\n")

def generate_queries(n=20):
    samples = []
    generated_date = date.today().isoformat()
    # Generate 'concern/urgent' and potentially multi-label 'question'
    for _ in range(n):
        template = random.choice(concern_templates)
        sample = {
            "text": template.format(
                event=random.choice(concern_events),
                symptom=random.choice(concern_symptoms),
                action=random.choice(concern_actions),
                medication="pill",
                situation=random.choice(concern_events),
                claim=random.choice(belief_claims),
                partner=random.choice(inclusive_partner_phrases),
                emotional=random.choice(emotional_phrases)
            ),
            "labels": ["concern/urgent", "question"],
            "source": "synthetic",
            "generator": "generate_minority_queries_ethical.py",
            "date_generated": generated_date
        }
        samples.append(sample)
    # Generate 'belief/claim/statement' and 'needs verification'
    for _ in range(n):
        template = random.choice(belief_templates)
        sample = {
            "text": template.format(claim=random.choice(belief_claims)),
            "labels": ["belief/claim/statement"],
            "source": "synthetic",
            "generator": "generate_minority_queries_ethical.py",
            "date_generated": generated_date
        }
        samples.append(sample)
    for _ in range(n):
        template = random.choice(needs_verification_templates)
        sample = {
            "text": template.format(claim=random.choice(belief_claims)),
            "labels": ["needs verification"],
            "source": "synthetic",
            "generator": "generate_minority_queries_ethical.py",
            "date_generated": generated_date
        }
        samples.append(sample)
    return samples

if __name__ == "__main__":
    output_file = "minority_queries.jsonl"
    n = 20
    approved = 0
    while approved < n:
        # Randomly pick which class to generate
        class_type = random.choice(["concern", "belief", "needs_verification"])
        generated_date = date.today().isoformat()
        if class_type == "concern":
            template = random.choice(concern_templates)
            sample = {
                "text": template.format(
                    event=random.choice(concern_events),
                    symptom=random.choice(concern_symptoms),
                    action=random.choice(concern_actions),
                    medication="pill",
                    situation=random.choice(concern_events),
                    claim=random.choice(belief_claims),
                    partner=random.choice(inclusive_partner_phrases),
                    emotional=random.choice(emotional_phrases)
                ),
                "labels": ["concern/urgent", "question"],
                "source": "synthetic",
                "generator": "generate_minority_queries_ethical.py",
                "date_generated": generated_date
            }
        elif class_type == "belief":
            template = random.choice(belief_templates)
            sample = {
                "text": template.format(claim=random.choice(belief_claims)),
                "labels": ["belief/claim/statement"],
                "source": "synthetic",
                "generator": "generate_minority_queries_ethical.py",
                "date_generated": generated_date
            }
        else:
            template = random.choice(needs_verification_templates)
            sample = {
                "text": template.format(claim=random.choice(belief_claims)),
                "labels": ["needs verification"],
                "source": "synthetic",
                "generator": "generate_minority_queries_ethical.py",
                "date_generated": generated_date
            }
        resp = prompt_user(sample)
        if resp == "y":
            append_to_file(sample, output_file)
            approved += 1
            print(f"Added ({approved}/{n})")
        elif resp == "q":
            print("Quitting early.")
            break
        else:
            print("Skipped.")
    print(f"Session complete. {approved} queries added to {output_file}.")