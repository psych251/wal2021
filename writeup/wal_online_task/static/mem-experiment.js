var jsPsych = initJsPsych({
    show_progress_bar: true,
    on_finish: function() {

        var form = document.createElement("form");
        form.setAttribute('method',"POST");
        form.setAttribute('id',"exp");

        var input = document.createElement("input");
        input.setAttribute("type", "hidden");
        input.setAttribute("id", "experimentResults");
        input.setAttribute("name", "experimentResults");
        input.setAttribute("value", "[]");
        form.appendChild(input);

        var interact = document.createElement("input");
        interact.setAttribute("type", "hidden");
        interact.setAttribute("id", "interactionData");
        interact.setAttribute("name", "interactionData");
        interact.setAttribute("value", "[]");
        form.appendChild(interact);

        document.body.appendChild(form);

        var strExpResults = jsPsych.data.get().json();
        document.getElementById('experimentResults').value = strExpResults;

        var strInteractData = jsPsych.data.getInteractionData().json();
        document.getElementById('interactionData').value = strInteractData;

        document.getElementById('exp').submit();
    }
});

// Define timeline.
var timeline = [];

timeline.push({
  type: jsPsychFullscreen,
  fullscreen_mode: true
});

var practice_verbs = ["modify","sculpt","construct","integrate"];
var practice_imgs = ["/static/for_instructions/object_pics/drawing_bird/heron.jpg",
                        "/static/for_instructions/object_pics/picture_electronic/flashlight.jpg",
                        "/static/for_instructions/object_pics/drawing_clothe/hockey helmet.jpg",
                        "/static/for_instructions/object_pics/picture_veggie/avocado.jpg"];
var practice_instructions = ["semantic","perceptual","semantic","perceptual"];

/* preload images */
var preload = {
  type: jsPsychPreload,
  images: imgs.concat(practice_imgs).concat(["/static/instructions_pics/encoding_pic.png",
                                            "/static/instructions_pics/retrieval_pic.png"]),
};
timeline.push(preload);

var encoding_practice_instructions = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: `
    <p>In this part of the study, you will first see an action verb. This will be followed by a plus sign, and then an object.<br>
    Your job is to create a vivid mental image involving the action verb and the object.<br>
    Once you have a clear association in mind, press the space bar to continue to the next trial.<br>
    <br>
    Please keep in mind that you will be asked later about the object\'s perceptual properties in addition to its meaning.
    This may include questions regarding the color or shape of the objects.
    <br>
    <img src="/static/instructions_pics/encoding_pic.png" height="200px">
    <br>
    Now, you will first do some practice trials. Press the space bar when you are ready to continue.</p>`,
  choices: [' ']
};
timeline.push(encoding_practice_instructions);

for (var i=0; i<practice_verbs.length; i++) {
    const encoding_trial = {
        type: encodingTrialPlugin,
        cue: practice_verbs[i],
        associate: practice_imgs[i],
        is_practice: 1,
    }
    timeline = timeline.concat(encoding_trial);
}

var retrieval_practice_instructions = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: `
    <p>Great job!
    <br>
    Now you will see an action verb that you were shown earlier. Your job is to bring back to mind the object
    that you imagined being involved with this word and to report information about the object\'s semantic or visual features.
    <br>
    A question screen presented before the action verb will indicate which feature you are to report on:
    <br>
    "animate vs. inanimate" or "photo vs. drawing".
    <br>
    Press the left arrow button for animate/photo or the right arrow button for inanimate/drawing.
    <br>
    If you forgot the object associated with the verb, press the down arrow.
    Please respond as quickly as possible, and use your dominant hand to make your responses.
    <br>
    <img src="/static/instructions_pics/retrieval_pic.png" height="350px">
    <br>When you read the first set of instructions, you may have created a vivid mental image involving the word "find" and a drawing of a dog.
    In these examples trials shown above, the correct response for the top row is "animate", whereas the correct response for the bottom row is "drawing".
    <br>When you are ready to begin, press the space bar.</p>`,
  choices: [' ']
};

timeline.push(retrieval_practice_instructions);

for (var i=0; i<practice_verbs.length; i++) {
    const retrieval_trial = {
        type: retrievalTrialPlugin,
        cue: practice_verbs[i],
        associate: practice_imgs[i],
        animacy: 'null',
        style: 'null',
        instruction_class: practice_instructions[i],
        instruction: practice_instructions[i] == 'semantic' ?
            '<p>animate (left)&emsp;&emsp;&emsp;&emsp;inanimate (right)<br><br>forgotten (down)</p>'
            : '<p>photo (left)&emsp;&emsp;&emsp;&emsp;drawing (right)<br><br>forgotten (down)</p>',
        prompt: ''
    }
    timeline = timeline.concat(retrieval_trial);
}

var quiz = {
    type: jsPsychSurveyMultiChoice,
    preamble: 'Here are some questions about the tasks. You must answer all questions correctly to continue.',
    questions: [
    {
        prompt: "In every trial of one task, I will have to create a vivid mental image involving an action verb and an object.",
        name: 'Encoding',
        options: ['True', 'False'],
        required: true
    },
    {
        prompt: "When I am creating a vivid mental image involving an action verb and an object, I should press the space bar as soon as I have a clear image in mind.",
        name: 'EncodingKeys',
        options: ['True', 'False'],
        required: true
    },
    {
        prompt: 'When I see an action verb on the screen, and my task is to bring back to mind the object I previously imagined being involved with this action verb, I will be asked about a semantic ("Was it animate or inanimate?") or perceptual ("was it a photo or a drawing?") feature of the object.',
        name: 'Retrieval',
        options: ['True', 'False'],
        required: true
    },
    {
        prompt: "When I see an action verb on the screen, and my task is to bring back to mind the object I previously imagined being involved with this action verb, I will use the arrow keys to make my response.",
        name: 'RetrievalKeys',
        options: ['True', 'False'],
        required: true
    }
    ],
}

var loop_node = {
    timeline: [quiz],
    loop_function: function(data){
        responses = data.values()[0].response;
        if (responses['Encoding'] == 'True' && responses['EncodingKeys'] == 'True' && responses['Retrieval'] == 'True' && responses['RetrievalKeys'] == 'True'){
            return false;
        } else {
            alert("At least one if your responses is incorrect. Please try again.");
            return true;
        }
    }
}

timeline.push(loop_node);

var msg = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: `
    <p>Great job! Now you\'ll continue onto doing the main tasks.
    You will have the opportunity to take brief breaks at various points.
    The instructions will be displayed again before the start of each task, in case you need a refresher.
    Good luck!<br>Press the space bar to continue.</p>`,
  choices: [' ']
};

timeline.push(msg);

timeline.push({
  type: jsPsychFullscreen,
  fullscreen_mode: true
});

var encoding_instructions = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: `
    <p>As you practiced earlier, you will first see an action verb in this part of the study. This will be followed by a plus sign, and then an object.<br>
    Your job is to create a vivid mental image involving the action verb and the object.<br>
    Once you have a clear association in mind, press the space bar to continue to the next trial.<br>
    <br>
    Please keep in mind that you will be asked later about the object\'s perceptual properties in addition to its meaning.
    <br>
    <img src="/static/instructions_pics/encoding_pic.png" height="350px">
    <br>
    Press the space bar when you are ready to start the task.</p>`,
  choices: [' ']
};

var numbers_instructions = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: `
    <p>Now, you will a series of numbers. <br>
    If the number is even, press the left arrow key. <br>
    If the number is odd, press the right arrow key.<br>
    <br>
    When you are ready to begin, press the space bar.</p>`,
  choices: [' ']
};

const number_trials = {
    type: numberParityTrialPlugin,
    duration: 20000,
}

/* define welcome message trial */
var retrieval_instructions = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: `
    <br>
    As you practiced earlier, you will now see an action verb that you were shown earlier. Your job is to bring back to mind the object
    that you imagined being involved with this word and to report information about the object\'s semantic or visual features.
    <br>
    A question screen presented before the action verb will indicate which feature you are to report on:
    <br>
    "animate vs. inanimate" or "photo vs. drawing".
    <br>
    Press the left arrow button for animate/photo or the right arrow button for inanimate/drawing.
    <br>
    If you forgot the object associated with the verb, press the down arrow.
    Please respond as quickly as possible, and use your dominant hand to make your responses.
    <br>
    <img src="/static/instructions_pics/retrieval_pic.png" height="350px">
    <br>When you read the first set of instructions, you may have created a vivid mental image involving the word "find" and a drawing of a dog.
    In these examples trials shown above, the correct response for the top row is "animate", whereas the correct response for the bottom row is "drawing".
    <br>When you are ready to begin, press the space bar.</p>`,
  choices: [' ']
}

var add_encoding_block_to_timeline = function(trial_i, trial_j) {
    for (var i=trial_i; i<trial_j; i++) {
        var trial = encoding_trials[i];
        const encoding_trial = {
            type: encodingTrialPlugin,
            cue: trial['verb'],
            associate: trial['img']
        }
    timeline.push(encoding_trial);
    }
}

var retrieval_feedback = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: function(){
    var n_trials_per_block = n_imgs_per_block * n_instructions;
    var percent_last_block_trials_correct = jsPsych.data.get().last(n_trials_per_block).select("accurate").mean() * 100;
    return "<p>In that last set of trials, you were correct " + percent_last_block_trials_correct.toFixed(0) + "% of the time.<br> Press the space bar to continue. </p>";
  },
  choices: [' ']
}

var add_retrieval_block_to_timeline = function(trial_i, trial_j) {
    var block_retrieval_trials = retrieval_trials.slice(trial_i,trial_j);
    for (var i=0; i<block_retrieval_trials.length; i++) {
        var trial = block_retrieval_trials[i];
        const retrieval_trial = {
            type: retrievalTrialPlugin,
            cue: trial['verb'],
            associate: trial['img'],
            animacy: trial['animacy'],
            style: trial['style'],
            instruction_class: trial['instruction'],
            instruction: trial['instruction'] == 'semantic' ?
            '<p>animate (left)&emsp;&emsp;&emsp;&emsp;inanimate (right)<br><br>forgotten (down)</p>'
            : '<p>photo (left)&emsp;&emsp;&emsp;&emsp;drawing (right)<br><br>forgotten (down)</p>',
            prompt: ''
        }
        timeline.push(retrieval_trial);
    }
    timeline.push(retrieval_feedback);
}

var numbers_feedback = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: function(){
    var mean_accuracy = jsPsych.data.get().last(1).values()[0].mean_accuracy * 100;
    return "<p>In that last set of trials, you were correct " + mean_accuracy.toFixed(0) + "% of the time.<br> Press the space bar to continue. </p>";
  },
  choices: [' ']
}

var n_imgs_per_block = 8;
var n_instructions = 2; // perceptual and semantic
// the number of retrieval trials per block is n_imgs_per_block * n_instructions
var n_blocks = encoding_trials.length / n_imgs_per_block;

for (var block_i=0;block_i<n_blocks;block_i++) {
    timeline.push(encoding_instructions);
    add_encoding_block_to_timeline(block_i*n_imgs_per_block,(block_i+1)*n_imgs_per_block);
    timeline.push(numbers_instructions);
    timeline.push(number_trials);
    timeline.push(numbers_feedback);
    timeline.push(retrieval_instructions);
    add_retrieval_block_to_timeline(block_i*n_imgs_per_block*n_instructions,(block_i+1)*n_imgs_per_block*n_instructions);
}

var debrief = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: `
    <p>Thank you for your participation!</p>
    The goal of this study is to replicate previous findings that the timing of responses in memory-dependent tasks
    is rhythmic in nature (compared to the timing of responses in memory-independent tasks).
    <br>
    Your participation will allow us to better understand how memory works.
    Please do not share this information with other potential participants.
    <br>
    Press the space bar to continue.</p>`,
  choices: [' ']
};
timeline.push(debrief);

/* start the trial */
jsPsych.run(timeline);