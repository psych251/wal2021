/**
 *
 * Plugin to run one trial of numbers (distractor) task
 *
**/

var numberParityTrialPlugin = (function(jsPsych) {
  "use strict";

  const info = {
    name: 'number-parity-trial',
    description: 'Indicate whether a number is odd or even.',
    parameters: {
        duration: {
            type: jsPsych.ParameterType.INT,
            description: 'Duration of number parity task.',
            default: 60000
        },
        valid_responses: {
            type: jsPsych.ParameterType.KEYCODE,
            description: 'Valid response buttons.',
            default: ["ArrowLeft","ArrowRight"]
        },
        max_number: {
            type: jsPsych.ParameterType.INT,
            description: 'Maximum number to be displayed.',
            default: 99
        }
    }
  }

  /**
   * **number-trial**
   *
   * Judge whether the numbers displayed are odd or even
   *
   * @author Alice Xue
   */
  class NumberParityTrialPlugin {
    constructor(jsPsych) {
      this.jsPsych = jsPsych;
    }

    trial(display_element, trial) {
        var keyboardListener = null;

        this.jsPsych.pluginAPI.setTimeout(() => {
            this.jsPsych.pluginAPI.clearAllTimeouts();
            this.jsPsych.pluginAPI.cancelKeyboardResponse(keyboardListener);
            var trial_data = {
                numbers: numbers,
                response: responses,
                trial_accuracies: trial_accuracies,
                mean_accuracy: trial_accuracies.reduce((a, b) => a + b, 0) / trial_accuracies.length,
            }
            this.jsPsych.finishTrial(trial_data);
        }, trial.duration)

        var numbers = [];
        var responses = [];
        var rts = [];
        var trial_accuracies = [];

        var number_display = () => {
          var rand_int = Math.round(Math.random() * (trial.max_number - 1) + 1);
          numbers.push(rand_int);
          display_element.innerHTML = '<p>' + rand_int + '</p><br><p>Is this number even (left arrow) or odd (right arrow)?</p>'
            keyboardListener = this.jsPsych.pluginAPI.getKeyboardResponse({
              callback_function: after_response,
              valid_responses: trial.valid_responses,
              rt_method: 'performance',
              persist: false,
              allow_held_key: false
            });
        }

        var after_response = (info) => {
            responses.push(info.key);
            rts.push(info.rt);
            var last_number = numbers[numbers.length-1];
            var correct_response = last_number % 2 ? trial.valid_responses[1] : trial.valid_responses[0];
            correct_response = correct_response.toLowerCase(); // because of the discrepancy in capitalization in key input and in info
            var accuracy = correct_response == info.key;
            trial_accuracies.push(accuracy);
            number_display();
        }

        number_display();
      }
    }
    NumberParityTrialPlugin.info = info;

    return NumberParityTrialPlugin;
})(jsPsychModule);