"""
Deep Space Command (DSC) — Mission Safety & Ethics Demo
Version: 1.0.0
Author: Captain Leif W. Sogge (Space LEAF Corp)
Status: Demonstration / Non-flight, Non-operational

Description:
    This module provides a structured, ethics-first example of how a
    Deep Space Command–style system might evaluate missions for
    safety, ethical compliance, and coordination readiness.

    This is NOT a NASA or government system.
    It is a civilian, educational, and conceptual demo intended
    for open discussion, learning, and future refinement.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Optional
import datetime
import logging


# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | DSC | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# ---------------------------------------------------------------------------
# Core domain models
# ---------------------------------------------------------------------------

class MissionPhase(Enum):
    PLANNING = auto()
    PRELAUNCH = auto()
    CRUISE = auto()
    OPERATIONS = auto()
    RETURN = auto()
    ARCHIVE = auto()


class EthicsStatus(Enum):
    PENDING_REVIEW = auto()
    APPROVED = auto()
    REJECTED = auto()


class SafetyStatus(Enum):
    UNKNOWN = auto()
    MARGINAL = auto()
    ACCEPTABLE = auto()
    UNACCEPTABLE = auto()


@dataclass
class DeepSpaceCorridor:
    """
    Represents a conceptual "corridor" of deep space where operations
    are planned. This is intentionally abstract and non-coordinate-specific
    to avoid implying real navigation authority.
    """
    name: str
    description: str
    sensitivity_level: int  # 1 = low, 5 = extremely sensitive
    protected_assets: List[str] = field(default_factory=list)


@dataclass
class MissionEthicsProfile:
    """
    Captures the ethical framing of a mission.
    """
    civilian_safety_priority: bool
    environmental_stewardship: bool
    data_transparency_plan: bool
    child_audience_considered: bool
    notes: str = ""


@dataclass
class MissionSafetyProfile:
    """
    Captures the safety posture of a mission.
    """
    redundancy_level: int  # 0–5
    abort_options_available: bool
    crewed: bool
    autonomous_systems_involved: bool
    notes: str = ""


@dataclass
class DeepSpaceMission:
    """
    High-level representation of a deep-space mission concept.
    """
    mission_id: str
    name: str
    phase: MissionPhase
    corridor: DeepSpaceCorridor
    ethics_profile: MissionEthicsProfile
    safety_profile: MissionSafetyProfile
    ethics_status: EthicsStatus = EthicsStatus.PENDING_REVIEW
    safety_status: SafetyStatus = SafetyStatus.UNKNOWN
    created_at: datetime.datetime = field(default_factory=datetime.datetime.utcnow)


# ---------------------------------------------------------------------------
# Evaluation engines
# ---------------------------------------------------------------------------

class EthicsEvaluator:
    """
    Evaluates a mission's ethical posture based on a simple rule set.
    In a real system, this would be replaced with a formal framework
    and multi-stakeholder review.
    """

    @staticmethod
    def evaluate(mission: DeepSpaceMission) -> EthicsStatus:
        logging.info(f"Evaluating ethics for mission: {mission.mission_id}")

        profile = mission.ethics_profile
        score = 0

        if profile.civilian_safety_priority:
            score += 2
        if profile.environmental_stewardship:
            score += 2
        if profile.data_transparency_plan:
            score += 1
        if profile.child_audience_considered:
            score += 1

        # Simple threshold logic for demo purposes
        if score >= 5:
            status = EthicsStatus.APPROVED
        elif score >= 3:
            status = EthicsStatus.PENDING_REVIEW
        else:
            status = EthicsStatus.REJECTED

        logging.info(
            f"Ethics evaluation complete | Mission={mission.mission_id} | Score={score} | Status={status.name}"
        )
        return status


class SafetyEvaluator:
    """
    Evaluates a mission's safety posture based on redundancy, abort options,
    and whether the mission is crewed.
    """

    @staticmethod
    def evaluate(mission: DeepSpaceMission) -> SafetyStatus:
        logging.info(f"Evaluating safety for mission: {mission.mission_id}")

        profile = mission.safety_profile
        score = 0

        # Redundancy is king in spaceflight
        score += profile.redundancy_level

        if profile.abort_options_available:
            score += 2

        if profile.crewed:
            # Crewed missions require higher safety margins
            score -= 1

        if profile.autonomous_systems_involved:
            # Autonomous systems can be a risk or a mitigation;
            # here we treat them neutrally and rely on redundancy.
            score += 0

        # Map score to status
        if score >= 6:
            status = SafetyStatus.ACCEPTABLE
        elif score >= 3:
            status = SafetyStatus.MARGINAL
        else:
            status = SafetyStatus.UNACCEPTABLE

        logging.info(
            f"Safety evaluation complete | Mission={mission.mission_id} | Score={score} | Status={status.name}"
        )
        return status


# ---------------------------------------------------------------------------
# Command-level decision logic
# ---------------------------------------------------------------------------

class DeepSpaceCommandCenter:
    """
    Central coordination object for evaluating and tracking missions.
    This is a conceptual "command" in the civilian stewardship sense:
    responsible, not authoritarian.
    """

    def __init__(self) -> None:
        self._missions: Dict[str, DeepSpaceMission] = {}

    def register_mission(self, mission: DeepSpaceMission) -> None:
        if mission.mission_id in self._missions:
            raise ValueError(f"Mission ID already registered: {mission.mission_id}")
        self._missions[mission.mission_id] = mission
        logging.info(f"Mission registered | ID={mission.mission_id} | Name={mission.name}")

    def evaluate_mission(self, mission_id: str) -> DeepSpaceMission:
        mission = self._get_mission(mission_id)

        mission.ethics_status = EthicsEvaluator.evaluate(mission)
        mission.safety_status = SafetyEvaluator.evaluate(mission)

        logging.info(
            "Mission evaluation summary | ID=%s | Ethics=%s | Safety=%s",
            mission.mission_id,
            mission.ethics_status.name,
            mission.safety_status.name,
        )

        return mission

    def go_no_go(self, mission_id: str) -> bool:
        mission = self._get_mission(mission_id)

        if mission.ethics_status != EthicsStatus.APPROVED:
            logging.warning(
                "NO-GO: Ethics not approved | Mission=%s | EthicsStatus=%s",
                mission.mission_id,
                mission.ethics_status.name,
            )
            return False

        if mission.safety_status not in (SafetyStatus.ACCEPTABLE, SafetyStatus.MARGINAL):
            logging.warning(
                "NO-GO: Safety unacceptable | Mission=%s | SafetyStatus=%s",
                mission.mission_id,
                mission.safety_status.name,
            )
            return False

        logging.info(
            "GO: Mission cleared for next planning phase | Mission=%s",
            mission.mission_id,
        )
        return True

    def _get_mission(self, mission_id: str) -> DeepSpaceMission:
        try:
            return self._missions[mission_id]
        except KeyError:
            raise KeyError(f"Mission not found: {mission_id}")


# ---------------------------------------------------------------------------
# Demo harness (for local testing and educational use)
# ---------------------------------------------------------------------------

def _build_demo_mission() -> DeepSpaceMission:
    corridor = DeepSpaceCorridor(
        name="Atlas Corridor",
        description="Conceptual deep-space corridor used for educational ethics and safety simulations.",
        sensitivity_level=3,
        protected_assets=["Microscopic travelers (conceptual)", "Scientific observation windows"],
    )

    ethics = MissionEthicsProfile(
        civilian_safety_priority=True,
        environmental_stewardship=True,
        data_transparency_plan=True,
        child_audience_considered=True,
        notes="Designed under Space LEAF Corp principles: kids first, planet first, no weapons.",
    )

    safety = MissionSafetyProfile(
        redundancy_level=4,
        abort_options_available=True,
        crewed=False,
        autonomous_systems_involved=True,
        notes="Simulation-only mission; no real hardware or flight operations.",
    )

    return DeepSpaceMission(
        mission_id="DSC-DEMO-001",
        name="Atlas Stewardship Simulation",
        phase=MissionPhase.PLANNING,
        corridor=corrior,
        ethics_profile=ethics,
        safety_profile=safety,
    )


def run_demo() -> None:
    logging.info("Starting Deep Space Command demo run")

    dsc = DeepSpaceCommandCenter()
    mission = _build_demo_mission()
    dsc.register_mission(mission)

    evaluated = dsc.evaluate_mission(mission.mission_id)
    decision = dsc.go_no_go(evaluated.mission_id)

    logging.info(
        "Final decision | Mission=%s | GO=%s",
        evaluated.mission_id,
        "YES" if decision else "NO",
    )

    logging.info("Deep Space Command demo run complete")


if __name__ == "__main__":
    run_demo()
