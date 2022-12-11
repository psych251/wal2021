/**
 *
 * Plugin to run one trial of visual task
 *
**/

var visualTrialPlugin = (function(jsPsych) {
  "use strict";

  const info = {
    name: 'visual-trial',
    description: 'Indicate whether the object is animate vs. inanimate or a drawing vs. photo.',
    parameters: {
        instruction: {
            type: jsPsych.ParameterType.HTML_STRING,
            description: 'Instruction to be displayed before cue (animate vs. inanimate or photo vs. drawing).'
        },
        instruction_class: {
            type: jsPsych.ParameterType.STRING,
            pretty_name: 'animacy/style',
            description: ''
        },
        instruction_duration: {
            type: jsPsych.ParameterType.INT,
            description: 'Duration of prompt presentation in ms.',
            default: 3000
        },
        prompt: {
            type: jsPsych.ParameterType.HTML_STRING,
            description: 'Prompt to be displayed under the cue.'
        },
        object: {
            type: jsPsych.ParameterType.HTML_STRING,
            pretty_name: 'Object',
            description: 'Filename of the object image in static folder.'
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
        object_duration: {
            type: jsPsych.ParameterType.INT,
            description: 'Duration of object presentation in ms.',
            default: 7000
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
   * Display instruction, make judgment about object
   *
   * @author Alice Xue
   */
  class VisualTrialPlugin {
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
          display_element.innerHTML = `<div style="font-size:60px;">+</div><br><br><p>${trial.instruction}</p>`;
          this.jsPsych.pluginAPI.setTimeout(()=>{
                object_display();
            }, trial.instruction_duration);
        }

        var object_display = () => {
            display_element.innerHTML = `<img src="${trial.object}" height="300"></img><br>${trial.prompt}`;
            keyboardListener = this.jsPsych.pluginAPI.getKeyboardResponse({
              callback_function: after_response,
              valid_responses: trial.valid_responses,
              rt_method: 'performance',
              persist: false,
              allow_held_key: false
            });
            this.jsPsych.pluginAPI.setTimeout(function() {
                after_response();
            }, trial.object_duration);
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

            info.instruction                = trial.instruction;
            info.instruction_class          = trial.instruction_class;
            info.instruction_duration       = trial.instruction_duration;
            info.prompt                     = trial.prompt;
            info.object                     = trial.object;
            info.object_duration            = trial.object_duration;
            info.animacy                    = trial.animacy;
            info.style                      = trial.style;
            info.jitter                     = jitter;
            var correct_response            = trial.instruction_class == 'semantic' ? trial.animacy : trial.style;
            var correct_response_key        = (correct_response == 'animate' || correct_response == 'photo') ? 'arrowleft' : 'arrowright';
            info.accurate                   = response.key == correct_response_key;

            // end trial
            this.jsPsych.finishTrial(info);
        }

        fixation_display();
      }
    }
    VisualTrialPlugin.info = info;

    return VisualTrialPlugin;
})(jsPsychModule);