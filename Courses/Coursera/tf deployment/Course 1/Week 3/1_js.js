const threshold = 0.9;

function approx(num) {
    num *= 100;
    num = Math.round(num);
    num /= 100;
    return num;
}

toxicity.load(threshold).then((model) => {
    const sentences = ['you suck!'];
    model.classify(sentences).then(predictions => {
        //Iterating over all returned results
        for (i = 0; i < 7; i++) {
            if (predictions[i].results[0].match) {
                str = (predictions[i].label) + " was found with a probability of " +
                    approx(predictions[i].results[0].probabilities[1]);
                console.log(str);
                // alert(str);
            };
        }
    });
})