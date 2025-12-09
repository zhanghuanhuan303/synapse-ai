"""
Core conceptual definitions for Synapse.
This file defines the key abstractions before implementation.
"""

from typing import Protocol, runtime_checkable
from dataclasses import dataclass
from enum import Enum

# ======================
# Core Abstractions
# ======================

class DocumentElementType(Enum):
    """Types of document elements our system recognizes"""
    IDEA_FRAGMENT = "idea_fragment"
    ARGUMENT = "argument"
    EVIDENCE = "evidence"
    CONCLUSION = "conclusion"
    TRANSITION = "transition"  # How ideas connect
    
    # Traditional elements
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST = "list"
    
    # Academic elements
    ABSTRACT = "abstract"
    REFERENCE = "reference"
    THEOREM = "theorem"
    PROOF = "proof"

@dataclass
class CognitiveFlowMetric:
    """Metrics for measuring idea flow quality"""
    interruption_frequency: float  # How often formatting interrupts thinking
    idea_density: float  # Ideas per unit time
    coherence_score: float  # How well ideas connect
    expression_clarity: float  # How clearly ideas are expressed

# ======================
# Core Protocols (Interfaces)
# ======================

@runtime_checkable
class IdeaProcessor(Protocol):
    """Protocol for processing raw ideas into structured content"""
    
    def capture_idea_fragment(self, raw_input: str) -> dict:
        """Capture a spontaneous idea fragment"""
        ...
    
    def find_connections(self, idea_a: dict, idea_b: dict) -> list[str]:
        """Find conceptual connections between ideas"""
        ...
    
    def suggest_structure(self, ideas: list[dict]) -> dict:
        """Suggest how ideas might organize into a document"""
        ...

@runtime_checkable  
class FormattingDelegate(Protocol):
    """Protocol for delegating formatting decisions to AI"""
    
    def should_interrupt(self, context: dict) -> bool:
        """Decide if now is a good time for formatting feedback"""
        ...
    
    def suggest_improvements(self, content: str, focus: str = "clarity") -> list[str]:
        """Suggest improvements without disrupting flow"""
        ...

# ======================
# Key Design Decisions
# ======================

SYNAPSE_DESIGN_PRINCIPLES = {
    "cognitive_flow_first": "Never interrupt the user's train of thought",
    "transparent_automation": "AI decisions should be explainable",
    "progressive_enhancement": "Basic functionality works everywhere",
    "idea_sovereignty": "The user owns and controls all ideas",
}

# ======================
# Data Structures
# ======================

@dataclass
class IdeaNode:
    """Represents a single idea in the thought graph"""
    id: str
    content: str
    type: DocumentElementType
    connections: list[str]  # IDs of connected ideas
    metadata: dict
    created_at: float
    modified_at: float
    
    def to_document_element(self, style: str = "academic") -> dict:
        """Convert this idea to a document element in given style"""
        # This is where the "synapse" happens:
        # Idea → Document element transformation
        ...

@dataclass
class ThoughtGraph:
    """Graph structure representing connections between ideas"""
    nodes: dict[str, IdeaNode]
    edges: dict[tuple[str, str], dict]  # Edge metadata
    
    def find_best_structure(self) -> list[list[IdeaNode]]:
        """Find the most coherent document structure from the idea graph"""
        # Implements the core "synapse" algorithm
        ...
