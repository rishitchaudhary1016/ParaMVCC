from knowledge_editing_engine import KnowledgeEditingEngine

engine = KnowledgeEditingEngine()

result = engine.create_edit(
    question="When was the inception of IAAF Combined Events Challenge?",
    subject="IAAF Combined Events Challenge",
    answer="2015"
)

print(result)