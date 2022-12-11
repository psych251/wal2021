/**
 *
 * Plugin to run one trial of retrieval task
 *
**/

var retrievalTrialPlugin = (function(jsPsych) {
  "use strict";

  const info = {
    name: 'retrieval-trial',
    description: 'Recall the object (animate vs. inanimate; drawing vs. photo) associated with a verb cue',
    parameters: {
        cue: {
            type: jsPsych.ParameterType.STRING,
            pretty_name: 'Verb cue',
            description: 'The verb to be used as a cue.'
        },
        associate: {
            type: jsPsych.ParameterType.HTML_STRING,
            pretty_name: 'Associate object',
            description: 'Filename of the object associate in static folder.'
        },
        animacy: {
            type: jsPsych.ParameterType.STRING,
            pretty_name: 'Animacy',
            description: 'animate/inanimate'
        },
        style: {
            type: jsPsych.ParameterType.STRING,
            pretty_name: 'Style',
            description: 'photo/drawing'
        },
        instruction_class: {
            type: jsPsych.ParameterType.STRING,
            pretty_name: 'animacy/style',
            description: ''
        },
        instruction: {
            type: jsPsych.ParameterType.HTML_STRING,
            description: 'Instruction display (animate vs. inanimate; drawing vs. photo).'
        },
        prompt: {
            type: jsPsych.ParameterType.HTML_STRING,
            description: 'Prompt to be displayed under the cue.'
        },
        cue_duration: {
            type: jsPsych.ParameterType.INT,
            description: 'Duration of cue presentation in ms.',
            default: 10000
        },
        instruction_duration: {
            type: jsPsych.ParameterType.INT,
            description: 'Duration of instruction presentation in ms.',
            default: 3000
        },
        valid_responses: {
            type: jsPsych.ParameterType.KEYCODE,
            description: 'Valid response buttons.',
            default: ["ArrowLeft","ArrowRight","ArrowDown"]
        },
        min_jitter: {
            type: jsPsych.ParameterType.INT,
            description: 'Minimum jitter duration in ms.',
            default: 500
        },
        max_jitter: {
            type: jsPsych.ParameterType.INT,
            description: 'Maximum jitter duration in ms.',
            default: 1500
        },
    }
  }

  /**
   * **retrieval-trial**
   *
   * Display cue, recall associate
   *
   * @author Alice Xue
   */
  class RetrievalTrialPlugin {
    constructor(jsPsych) {
      this.jsPsych = jsPsych;
    }

    trial(display_element, trial) {
        var jitter = Math.random() * (trial.max_jitter - trial.min_jitter) + trial.min_jitter;
        var keyboardListener = null;

        var fixation_display = () => {
            display_element.innerHTML = '<div style="font-size:60px;">+</div>';
            this.jsPsych.pluginAPI.setTimeout(()=>{
                instruction_display();
            }, jitter);
        }

        var instruction_display = () => {
          display_element.innerHTML = `<br><br><div style="font-size:60px;">+</div><br><br><p>${trial.instruction}</p>`;
          this.jsPsych.pluginAPI.setTimeout(()=>{
                cue_display();
            }, trial.instruction_duration);
        }

        var cue_display = () => {
            display_element.innerHTML = `<p>${trial.cue}<br>${trial.prompt}</p>`;
            keyboardListener = this.jsPsych.pluginAPI.getKeyboardResponse({
              callback_function: after_response,
              valid_responses: trial.valid_responses,
              rt_method: 'performance',
              persist: false,
              allow_held_key: false
            });
            this.jsPsych.pluginAPI.setTimeout(function() {
                after_response();
            }, trial.cue_duration);
        }

        var response = {
          rt: -1,
          key: -1
        }

        var after_response = (info) => {
            // Kill any timeout handlers / keyboard listeners
            this.jsPsych.pluginAPI.clearAllTimeouts();
            this.jsPsych.pluginAPI.cancelKeyboardResponse(keyboardListener);

            // Record response (if any made)
            if (info != null) {
                response = info;
            } else {
                info = {};
            }

            info.cue                    = trial.cue;
            info.associate              = trial.associate;
            info.animacy                = trial.animacy;
            info.style                  = trial.style;
            info.instruction            = trial.instruction_class;
            info.instruction_text       = trial.instruction;
            info.prompt                 = trial.prompt;
            info.cue_duration           = trial.cue_duration;
            info.instruction_duration   = trial.instruction_duration;
            info.prompt_duration        = trial.prompt_duration;
            var correct_response        = trial.instruction_class == 'animacy' ? trial.animacy : trial.style;
            var correct_response_key    = (correct_response == 'animate' || correct_response == 'photo') ? 'arrowleft' : 'arrowright';
            info.accurate               = response.key == correct_response_key;

            // end trial
            this.jsPsych.finishTrial(info);
        }

        fixation_display();
      }
    }
    RetrievalTrialPlugin.info = info;

    return RetrievalTrialPlugin;
})(jsPsychModule);