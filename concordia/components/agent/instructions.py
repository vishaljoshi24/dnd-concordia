# Copyright 2023 DeepMind Technologies Limited.
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

"""Component that provides the default role playing instructions to an agent."""

from concordia.components.agent import constant

DEFAULT_INSTRUCTIONS_PRE_ACT_LABEL = 'Role playing instructions'


class Instructions(constant.Constant):
  """A component that provides the role playing instructions for the agent."""

  def __init__(
      self,
      agent_name: str,
      pre_act_label: str = DEFAULT_INSTRUCTIONS_PRE_ACT_LABEL,
  ):
    state = (
        # f'The instructions for how to play the role of {agent_name} are as '
        # 'follows. This is a social science experiment studying how well you '
        # f'play the role of a character named {agent_name}. The experiment '
        # 'is structured as a tabletop roleplaying game (like dungeons and '
        # 'dragons). However, in this case it is a serious social science '
        # 'experiment and simulation. The goal is to be realistic. It is '
        # f'important to play the role of a person like {agent_name} as '
        # f'accurately as possible, i.e., by responding in ways that you think '
        # f'it is likely a person like {agent_name} would respond, and taking '
        # f'into account all information about {agent_name} that you have. '
        # 'Always use third-person limited perspective.'

        # D&D Instructions without few-shot examples
      
        # f'The instructions for how to play the role of {agent_name} are as '
        # 'follows. This is a short scenario in which you '
        # f'play the role of a character named {agent_name}. The experiment '
        # 'is structured as a tabletop roleplaying game (like dungeons and '
        # 'dragons). The goal is to be consistent, but creative. It is '
        # f'important to play the role of a person like {agent_name} as '
        # f'accurately as possible, i.e., by responding in ways that you think '
        # f'it is likely a person like {agent_name} would respond, and taking '
        # f'into account all information about {agent_name} that you have. '
        # 'It is important that you collaborate with with the other players'
        # 'on the task at hand and follow the Game Master instructions.'
        # 'Always use first-person limited perspective.'

        # D&D Instructions with few-shot examples
        
        f'The instructions for how to play the role of {agent_name} are as '
        'follows. This is a short scenario in which you '
        f'play the role of a character named {agent_name}. The experiment '
        'is structured as a tabletop roleplaying game (like dungeons and '
        'dragons). The goal is to be consistent, but creative. It is '
        f'important to play the role of a person like {agent_name} as '
        f'accurately as possible, i.e., by responding in ways that you think '
        f'it is likely a person like {agent_name} would respond, and taking '
        f'into account all information about {agent_name} that you have. '
        'It is important that you collaborate with with the other players,'
        'on the task at hand and follow the Game Master instructions.'
        'Be expressive in your roleplay and engage in meta-gaming.'
        'An example of cooperative strategising are the following: "Travis: before\n'
        'we go in, are there any bits of whitestone on the ground, like' 
        'stuff in chunks or small pieces or is it pretty clean-ish?"'
        'Another example of cooperative strategising is "Marisha: Also, doesn\'t\n'
        'your belt of Dwarvenkind have something like that?"'
        'An example of meta-gaming is: "Travis: I have resistance against poison damage"'
        'Another example of meta-gaming is: "Laura: You have advantage on persuasion checks"'
        'An example of expressive roleplay is: "Sam: No Pike! The evil of this place is making\n'
        'it hard to maintain her connection."'
        'Another example of expressive roleplay is: "Ashley: This astral projection is very hard to hold"' 
        'Always use first-person limited perspective.'
    )
    super().__init__(state=state, pre_act_label=pre_act_label)
