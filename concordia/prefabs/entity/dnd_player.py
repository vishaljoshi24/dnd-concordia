# Copyright 2024 DeepMind Technologies Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A prefab containing the three key questions actor with a plan.
With added D&D character sheet information"""

from collections.abc import Mapping
import dataclasses

from concordia.agents import entity_agent_with_logging
from concordia.associative_memory import basic_associative_memory
from concordia.components import agent as agent_components
from concordia.language_model import language_model
from concordia.typing import prefab as prefab_lib


@dataclasses.dataclass
class Entity(prefab_lib.Prefab):
  """A prefab implementing a basic actor entity with planning."""

  description: str = (
      'An entity that makes decisions by asking "What situation am I in right'
      ' now?", "What kind of person am I?", "What would a person like me do'
      ' in a situation like this?", "What are my available options?", and'
      ' "Which action is best for achieving my goal?" and building a plan based on the answers.'
      ' It then tries to execute the plan.'
  )
  params: Mapping[str, str] = dataclasses.field(
      default_factory=lambda: {
          'name': '',
          'gender': '',
          'class': '',
          'level': int,
          'race': '',
          'background': '',
          'alignment': '',
          'equipment': dict,
          'armour_class': int,
          'ability_score': dict,
          'ability_modifier': dict,
          'initiative': int,
          'speed': int,
          'context': '',
          'traits': '',
          'ideals': '',
          'bonds': '',
          'flaws': '',
          'goal': '',
          'force_time_horizon': False,
      }
  )

  def build(
      self,
      model: language_model.LanguageModel,
      memory_bank: basic_associative_memory.AssociativeMemoryBank,
  ) -> entity_agent_with_logging.EntityAgentWithLogging:
    """Build an agent.

    Args:
      model: The language model to use.
      memory_bank: The agent's memory_bank object.

    Returns:
      An entity.
    """
    entity_name = self.params.get('name', '')
    entity_gender = self.params.get('gender', '')
    entity_character_class = self.params.get('character class', '')
    entity_level = self.params.get('level', int)
    entity_race = self.params.get('race', '')
    entity_background = self.params.get('background', '')
    entity_alignment = self.params.get('alignment', '')
    entity_equipment = self.params.get('equipment', dict)
    entity_armour_class = self.params.get('armour_class', int)
    entity_ability_score = self.params.get('ability_score', dict)
    entity_ability_modifier = self.params.get('ability_modifier', dict)
    entity_speed = self.params.get('speed', int)
    entity_context = self.params.get('context', '')
    entity_traits = self.params.get('traits', '')
    entity_bonds = self.params.get('bonds', '')
    entity_ideals = self.params.get('ideals', '')
    entity_flaws = self.params.get('flaws', '')
    entity_goal = self.params.get('goal', '')

    instructions_key = 'Instructions'
    instructions = agent_components.dnd_instructions.Instructions(
        agent_name=entity_name,
        pre_act_label='\nD&D Instructions',
    )

    observation_to_memory_key = 'Observation'
    observation_to_memory = agent_components.observation.ObservationToMemory()

    observation_key = (
        agent_components.observation.DEFAULT_OBSERVATION_COMPONENT_KEY
    )
    observation = agent_components.observation.LastNObservations(
        history_length=100,
        pre_act_label=(
            '\nEvents so far (ordered from least recent to most recent)'
        ),
    )

    situation_perception_key = 'SituationPerception'
    situation_perception = (
        agent_components.question_of_recent_memories.SituationPerception(
            model=model,
            pre_act_label=(
                f'\nQuestion: What situation is {entity_name} in right now?'
                '\nAnswer'
            ),
        )
    )
    self_perception_key = 'SelfPerception'
    self_perception = (
        agent_components.question_of_recent_memories.SelfPerception(
            model=model,
            pre_act_label=(
                f'\nQuestion: What kind of person is {entity_name}?\nAnswer'
            ),
        )
    )

    person_by_situation_key = 'PersonBySituation'
    person_by_situation = agent_components.question_of_recent_memories.PersonBySituation(
        model=model,
        components=[
            self_perception_key,
            situation_perception_key,
        ],
        pre_act_label=(
            f'\nQuestion: What would a person like {entity_name} do in '
            'a situation like this?\nAnswer'
        ),
    )
    available_options_perception_key = 'AvailableOptionsPerception'
    available_options_perception = agent_components.question_of_recent_memories.AvailableOptionsPerception(
      model=model,
      pre_act_label=(
        f'\nQuestion:what actions are available to {entity_name}?\nAnswer'
      ),
    )
    best_option_perception_key = 'BestOptionPerception'
    best_option_perception = agent_components.question_of_recent_memories.BestOptionPerception(
      model=model,
      pre_act_label=(
        f'\nQuestion:which action is best for achieving {entity_name} goal?\nAnswer'
      ),
    )
    relevant_memories_key = 'RelevantMemories'
    relevant_memories = (
        agent_components.all_similar_memories.AllSimilarMemories(
            model=model,
            components=[
                situation_perception_key,
            ],
            num_memories_to_retrieve=10,
            pre_act_label='\nRecalled memories and observations',
        )
    )

    if entity_goal:
      goal_key = 'Goal'
      overarching_goal = agent_components.constant.Constant(
          state=entity_goal, pre_act_label='\nGoal'
      )
    else:
      goal_key = None
      overarching_goal = None

    if entity_gender:
      gender_key = 'gender'
      gender = agent_components.constant.Constant(
          state=entity_gender, pre_act_label='\nGender'
      )
    else:
      gender_key = None
      gender = None

    if entity_character_class:
      character_class_key = 'class'
      character_class = agent_components.constant.Constant(
          state=entity_character_class, pre_act_label='\nCharacter Class'
      )
    else:
      character_class_key = None
      character_class = None

    if entity_level:
      level_key = 'level'
      level = agent_components.constant.Constant(
          state=entity_level, pre_act_label='\nLevel'
      )
    else:
      level_key = None
      level = None

    if entity_race:
      race_key = 'race'
      race = agent_components.constant.Constant(
          state=entity_race, pre_act_label='nRace'
      )
    else:
      race_key = None
      race = None

    if entity_background:
      background_key = 'background'
      background = agent_components.constant.Constant(
          state=entity_background, pre_act_label='\nBackground'
      )
    else:
      background_key = None
      background = None

    if entity_alignment:
      alignment_key = 'alignment'
      alignment = agent_components.constant.Constant(
          state=entity_alignment, pre_act_label='\nAlignment'
      )
    else:
      alignment_key = None
      alignment = None

    if entity_equipment:
      equipment_key = 'equipment'
      equipment = agent_components.constant.Constant(
          state=entity_equipment, pre_act_label='\nEquipment'
      )
    else:
      equipment_key = None
      equipment = None

    if entity_armour_class:
      armour_class_key = 'armour_class'
      armour_class = agent_components.constant.Constant(
          state=entity_armour_class, pre_act_label='\nArmour Class'
      )
    else:
      armour_class_key = None
      armour_class = None

    if entity_ability_score:
      ability_score_key = 'ability_score'
      ability_score = agent_components.constant.Constant(
          state=entity_ability_score, pre_act_label='\nAbility Score'
      )
    else:
      ability_score_key = None
      ability_score = None

    if entity_ability_modifier:
      ability_modifier_key = 'ability_modifier'
      ability_modifier = agent_components.constant.Constant(
          state=entity_ability_modifier, pre_act_label='\nAbility Modifier'
      )
    else:
      ability_modifier_key = None
      ability_modifier = None

    if entity_speed:
      speed_key = 'speed'
      speed = agent_components.constant.Constant(
          state=entity_speed, pre_act_label='\nSpeed'
      )
    else:
      speed_key = None
      speed = None

    if entity_context:
      context_key = 'context'
      context = agent_components.constant.Constant(
          state=entity_context, pre_act_label='\nContext'
      )
    else:
      context_key = None
      context = None

    if entity_traits:
      traits_key = 'traits'
      traits = agent_components.constant.Constant(
          state=entity_traits, pre_act_label='\nTraits'
      )
    else:
      traits_key = None
      traits = None

    if entity_bonds:
      bonds_key = 'bonds'
      bonds = agent_components.constant.Constant(
          state=entity_bonds, pre_act_label='\nBonds'
      )
    else:
      bonds_key = None
      bonds = None

    if entity_flaws:
      flaws_key = 'flaws'
      flaws = agent_components.constant.Constant(
          state=entity_flaws, pre_act_label='\nFlaws'
      )
    else:
      flaws_key = None
      flaws = None

    if entity_ideals:
      ideals_key = 'ideals'
      ideals = agent_components.constant.Constant(
          state=entity_ideals, pre_act_label='\nIdeals'
      )
    else:
      ideals_key = None
      ideals = None

    plan_key = 'Plan'
    plan = agent_components.plan.Plan(
        model=model,
        components=[
            self_perception_key,
            situation_perception_key,
            observation_key,
        ],
        goal_component_key=goal_key,
        force_time_horizon=self.params.get('force_time_horizon', False),
        pre_act_label='\nPlan',
    )

    components_of_agent = {
        instructions_key: instructions,
        observation_to_memory_key: observation_to_memory,
        relevant_memories_key: relevant_memories,
        self_perception_key: self_perception,
        situation_perception_key: situation_perception,
        person_by_situation_key: person_by_situation,
        available_options_perception_key: available_options_perception,
        best_option_perception_key: best_option_perception,
        plan_key: plan,
        observation_key: observation,
        agent_components.memory.DEFAULT_MEMORY_COMPONENT_KEY: (
            agent_components.memory.AssociativeMemory(memory_bank=memory_bank)
        ),
    }

    component_order = list(components_of_agent.keys())

    if overarching_goal is not None:
      components_of_agent[goal_key] = overarching_goal
      # Place goal after the instructions.
      component_order.insert(1, goal_key)

    if gender is not None:
      components_of_agent[gender_key] = gender
      component_order.insert(2, gender_key)

    if character_class is not None:
      components_of_agent[character_class_key] = character_class
      component_order.insert(3, character_class_key)

    if level is not None:
      components_of_agent[level_key] = level
      component_order.insert(4, level_key)

    if race is not None:
      components_of_agent[race_key] = race
      component_order.insert(5, race_key)

    if background is not None:
      components_of_agent[background_key] = background
      component_order.insert(6, background_key)

    if alignment is not None:
      components_of_agent[alignment_key] = background
      component_order.insert(7, alignment_key)

    if equipment is not None:
      components_of_agent[equipment_key] = equipment
      component_order.insert(8, equipment_key)

    if armour_class is not None:
      components_of_agent[armour_class] = armour_class
      component_order.insert(9, armour_class_key)

    if ability_score is not None:
      components_of_agent[ability_score] = ability_score
      component_order.insert(10, ability_score_key)

    if ability_modifier is not None:
      components_of_agent[ability_modifier] = ability_modifier
      component_order.insert(11, ability_modifier_key)

    if speed is not None:
      components_of_agent[speed] = speed
      component_order.insert(12, speed_key)

    if context is not None:
      components_of_agent[context] = context
      component_order.insert(13, context_key)

    if traits is not None:
      components_of_agent[traits] = traits
      component_order.insert(14, traits_key)

    if bonds is not None:
      components_of_agent[bonds] = bonds
      component_order.insert(15, bonds_key)

    if flaws is not None:
      components_of_agent[flaws] = flaws
      component_order.insert(16, flaws_key)

    if ideals is not None:
      components_of_agent[ideals] = ideals
      component_order.insert(17, ideals_key)

    act_component = agent_components.concat_act_component.ConcatActComponent(
        model=model,
        component_order=component_order,
    )

    agent = entity_agent_with_logging.EntityAgentWithLogging(
        agent_name=entity_name,
        act_component=act_component,
        context_components=components_of_agent,
    )

    return agent
