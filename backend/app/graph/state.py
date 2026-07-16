from typing import TypedDict, Optional, List
class AgentState(TypedDict):
    question: str                      
    context: Optional[str]                
    sources: List[str]                    
    is_relevant: Optional[bool]             
    answer: str                      