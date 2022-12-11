/**
 *
 * Plugin to run one trial of encoding task
 *
**/

var encodingTrialPlugin = (function(jsPsych) {
  "use strict";

  const info = {
    name: 'encoding-trial',
    description: 'Associate a verb cue with an object (animate vs. inanimate; drawing vs. photo)',
    parameters: {
        is_practice: {
            type: jsPsych.ParameterType.KEYCODE,
            default: 0
        },
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
        cue_duration: {
            type: jsPsych.ParameterType.INT,
            description: 'Duration of cue presentation in ms.',
            default: 2000
        },
        associate_duration: {
            type: jsPsych.ParameterType.INT,
            description: 'Duration of associate presentation in ms.',
            default: 7000
        },
        valid_responses: {
            type: jsPsych.ParameterType.KEYCODE,
            description: 'Valid response buttons.',
            default: [" "]
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
   * **encoding-trial**
   *
   * Display cue, fixation, associate, and ITI
   *
   * @author Alice Xue
   */
  class EncodingTrialPlugin {
    constructor(jsPsych) {
      this.jsPsych = jsPsych;
    }

    trial(display_element, trial) {
        var jitter = Math.random() * (trial.max_jitter - trial.min_jitter) + trial.min_jitter;
        var keyboardListener = null;

        var fixation_display = () => {
            display_element.innerHTML = '<div style="font-size:60px;">+</div>';
            this.jsPsych.pluginAPI.setTimeout(()=>{
                cue_display();
            }, jitter);
        }

        var cue_display = () => {
          display_element.innerHTML = `<p>${trial.cue}</p>`;
          this.jsPsych.pluginAPI.setTimeout(()=>{
                fixation_isi_display();
            }, trial.cue_duration);
        }

        var jitter_isi = Math.random() * (trial.max_jitter - trial.min_jitter) + trial.min_jitter;
        var fixation_isi_display = () => {
          display_element.innerHTML = '<div style="font-size:60px;">+</div>';
            this.jsPsych.pluginAPI.setTimeout(()=>{
                associate_display();
            }, jitter_isi);
        }

        var associate_display = () => {
            display_element.innerHTML = `<img src="${trial.associate}" height="300"></img>`;
            keyboardListener = this.jsPsych.pluginAPI.getKeyboardResponse({
              callback_function: after_response,
              valid_responses: trial.valid_responses,
              rt_method: 'performance',
              persist: false,
              allow_held_key: false
            });
            this.jsPsych.pluginAPI.setTimeout(function() {
                after_response();
            }, trial.associate_duration);
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

            info.cue                = trial.cue;
            info.associate          = trial.associate;
            info.cue_duration       = trial.cue_duration;
            info.associate_duration = trial.associate_duration;
            info.initial_jitter     = jitter;
            info.cue_asso_jitter    = jitter_isi;

            // end trial
            this.jsPsych.finishTrial(info);
        }

        fixation_display();
      }
    }
    EncodingTrialPlugin.info = info;

    return EncodingTrialPlugin;
})(jsPsychModule);