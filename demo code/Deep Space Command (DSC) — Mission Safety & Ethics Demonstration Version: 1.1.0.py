"""
Deep Space Command (DSC) — Mission Safety & Ethics Demonstration
Version: 1.1.0
Author: Captain Leif W. Sogge — Space LEAF Corp (Civilian Stewardship Division)
Status: Educational / Non‑Flight / Non‑Operational

Purpose:
    This module demonstrates how Deep Space Command evaluates conceptual
    deep‑space missions using ethics‑first, safety‑first civilian standards.

    It reflects the values outlined in the DSC public charter:
        • Kids first
        • Planet first
        • No weapons
        • Radical transparency
        • Civilian stewardship over deep‑space activity

    This is NOT a NASA system, NOT a government system, and NOT a
    navigation authority. It is a community‑driven educational model
    designed to help adults explore responsible deep‑space coordination.

    All mission corridors, assets, and evaluations are fictional and
    symbolic. No real spacecraft, coordinates, or operational systems
    are represented.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict
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
    name: str
    description: str
    sensitivity_level: int  # 1–5
    protected_assets: List[str] = field(default_factory=list)


@dataclass
class MissionEthicsProfile:
    civilian_safety_priority: bool
    environmental_stewardship: bool
    data_transparency_plan: bool
    child_audience_considered: bool
    notes: str = ""


@dataclass
class MissionSafetyProfile:
    redundancy_level: int  # 0–5
    abort_options_available: bool
    crewed: bool
    autonomous_systems_involved: bool
    notes: str = ""


@dataclass
class DeepSpaceMission:
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
    @staticmethod
    def evaluate(mission: DeepSpaceMission) -> EthicsStatus:
        logging.info(f"Evaluating ethics | Mission={mission.mission_id}")

        p = mission.ethics_profile
        score = 0

        if p.civilian_safety_priority: score += 2
        if p.environmental_stewardship: score += 2
        if p.data_transparency_plan: score += 1
        if p.child_audience_considered: score += 1

        if score >= 5:
            status = EthicsStatus.APPROVED
        elif score >= 3:
            status = EthicsStatus.PENDING_REVIEW
        else:
            status = EthicsStatus.REJECTED

        logging.info(
            f"Ethics evaluation complete | Score={score} | Status={status.name}"
        )
        return status


class SafetyEvaluator:
    @staticmethod
    def evaluate(mission: DeepSpaceMission) -> SafetyStatus:
        logging.info(f"Evaluating safety | Mission={mission.mission_id}")

        p = mission.safety_profile
        score = p.redundancy_level

        if p.abort_options_available: score += 2
        if p.crewed: score -= 1

        if score >= 6:
            status = SafetyStatus.ACCEPTABLE
        elif score >= 3:
            status = SafetyStatus.MARGINAL
        else:
            status = SafetyStatus.UNACCEPTABLE

        logging.info(
            f"Safety evaluation complete | Score={score} | Status={status.name}"
        )
        return status


# ---------------------------------------------------------------------------
# Command center
# ---------------------------------------------------------------------------

class DeepSpaceCommandCenter:
    def __init__(self) -> None:
        self._missions: Dict[str, DeepSpaceMission] = {}

    def register_mission(self, mission: DeepSpaceMission) -> None:
        if mission.mission_id in self._missions:
            raise ValueError("Mission ID already exists")
        self._missions[mission.mission_id] = mission
        logging.info(f"Mission registered | {mission.mission_id} — {mission.name}")

    def evaluate_mission(self, mission_id: str) -> DeepSpaceMission:
        mission = self._missions[mission_id]
        mission.ethics_status = EthicsEvaluator.evaluate(mission)
        mission.safety_status = SafetyEvaluator.evaluate(mission)
        return mission

    def go_no_go(self, mission_id: str) -> bool:
        mission = self._missions[mission_id]

        if mission.ethics_status != EthicsStatus.APPROVED:
            logging.warning(
                f"NO‑GO: Ethics not approved | Status={mission.ethics_status.name}"
            )
            return False

        if mission.safety_status not in (SafetyStatus.ACCEPTABLE, SafetyStatus.MARGINAL):
            logging.warning(
                f"NO‑GO: Safety unacceptable | Status={mission.safety_status.name}"
            )
            return False

        logging.info("GO: Mission cleared for next planning phase")
        return True


# ---------------------------------------------------------------------------
# Demo missions
# ---------------------------------------------------------------------------

def build_good_mission() -> DeepSpaceMission:
    corridor = DeepSpaceCorridor(
        name="Atlas Corridor",
        description="Symbolic deep‑space corridor used for stewardship simulations.",
        sensitivity_level=3,
        protected_assets=["Microscopic travelers (conceptual)", "Observation windows"],
    )

    ethics = MissionEthicsProfile(
        civilian_safety_priority=True,
        environmental_stewardship=True,
        data_transparency_plan=True,
        child_audience_considered=True,
        notes="Aligned with DSC principles.",
    )

    safety = MissionSafetyProfile(
        redundancy_level=4,
        abort_options_available=True,
        crewed=False,
        autonomous_systems_involved=True,
    )

    return DeepSpaceMission(
        mission_id="DSC‑DEMO‑GOOD",
        name="Atlas Stewardship Simulation",
        phase=MissionPhase.PLANNING,
        corridor=corridor,
        ethics_profile=ethics,
        safety_profile=safety,
    )


def build_bad_mission() -> DeepSpaceMission:
    corridor = DeepSpaceCorridor(
        name="Unreviewed Sector",
        description="A conceptual region requiring high caution.",
        sensitivity_level=5,
        protected_assets=["Unmapped particulate fields"],
    )

    ethics = MissionEthicsProfile(
        civilian_safety_priority=False,
        environmental_stewardship=False,
        data_transparency_plan=False,
        child_audience_considered=False,
        notes="Fails all DSC ethical baselines.",
    )

    safety = MissionSafetyProfile(
        redundancy_level=0,
        abort_options_available=False,
        crewed=True,
        autonomous_systems_involved=False,
        notes="Fails all DSC safety baselines.",
    )

    return DeepSpaceMission(
        mission_id="DSC‑DEMO‑BAD",
        name="Unethical Hazard Test",
        phase=MissionPhase.PLANNING,
        corridor=corridor,
        ethics_profile=ethics,
        safety_profile=safety,
    )


# ---------------------------------------------------------------------------
# Demo runner
# ---------------------------------------------------------------------------

def run_demo() -> None:
    logging.info("Starting Deep Space Command demo")

    dsc = DeepSpaceCommandCenter()

    good = build_good_mission()
    bad = build_bad_mission()

    dsc.register_mission(good)
    dsc.register_mission(bad)

    logging.info("\n--- Evaluating GOOD mission ---")
    dsc.evaluate_mission(good.mission_id)
    dsc.go_no_go(good.mission_id)

    logging.info("\n--- Evaluating BAD mission ---")
    dsc.evaluate_mission(bad.mission_id)
    dsc.go_no_go(bad.mission_id)

    logging.info("Demo complete")


if __name__ == "__main__":
    run_demo()
