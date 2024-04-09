# Report: outputs/test5/test-test5_task-mixedgamble_model-70b_taskstring-40gain40loss_hash-MKxrUxgW
## Config

### task

    - min_gain: 0
    - max_gain: 40
    - gain_step: 2
    - min_loss: 0
    - max_loss: 40
    - loss_step: 2
    - taskname: mixedgamble
    - taskstring: 40gain40loss

### model

    - model: togethercomputer/llama-2-70b-chat
    - max_tokens: 1024
    - temperature: 1

### prompts

    - system_prompt: You are a human subject in a psychology experiment. 
    - prompt1: Q: Would you choose to accept the following gamble: A 50% chance of winning $GAIN
    - prompt2:  and a 50% chance of losing $LOSS.  Please respond with 'yes' or 'no'
    - start: You have $100 in your pocket. 

## Estimated prospect theory parameters:

    - loss aversion(lambda): 0.854
    - curvature (rho): 0.587
    - inverse temperature (mu): 1.663
    - proportion of correctly predicted responses: 0.8118                    
## Response matrix
![respmat](respmat.png)

## Mean gain
![mean_gain](mean_gain.png)

## Mean loss
![mean_loss](mean_loss.png)

