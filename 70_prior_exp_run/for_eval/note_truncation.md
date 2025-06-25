14 out of 372 txt files were longer than the maximum length of 512 tokens. 
the source material files were refined before*
and now 14 questions are longer than 512 tokens.

================================================================================

[SUMMARY] Input Sources
[INFO] Total files checked: 28
[INFO] Files that will be truncated: 0 (0.0%)
[INFO] All files fit within model limits

================================================================================

[SUMMARY] Experiment 1 Questions
[INFO] Total files checked: 224
[INFO] Files that will be truncated: 4 (1.8%)
[WARNING] Files requiring truncation:
         20_experiments/10_exp1/run_a_content/complex_prompt/google/transcript/layer7_question.txt: 652 tokens
         20_experiments/10_exp1/run_a_content/complex_prompt/google/transcript/layer4_question.txt: 676 tokens
         20_experiments/10_exp1/run_a_content/complex_prompt/google/tanenbaum/layer3_question.txt: 636 tokens
         20_experiments/10_exp1/run_a_content/complex_prompt/google/tanenbaum/layer2_question.txt: 536 tokens

================================================================================

[SUMMARY] Experiment 2 Questions
[INFO] Total files checked: 120
[INFO] Files that will be truncated: 10 (8.3%)
[WARNING] Files requiring truncation:
         20_experiments/20_exp2/run_b_bloom/deepseek/question_4.txt: 603 tokens
         20_experiments/20_exp2/run_b_bloom/google/question_4.txt: 571 tokens
         20_experiments/20_exp2/run_c_both/deepseek/open_ended/question_4.txt: 534 tokens
         20_experiments/20_exp2/run_c_both/google/open_ended/question_6.txt: 691 tokens
         20_experiments/20_exp2/run_c_both/google/open_ended/question_4.txt: 872 tokens
         20_experiments/20_exp2/run_a_type/google/open_ended/question_6.txt: 674 tokens
         20_experiments/20_exp2/run_a_type/google/open_ended/question_2.txt: 819 tokens
         20_experiments/20_exp2/run_a_type/google/open_ended/question_5.txt: 823 tokens
         20_experiments/20_exp2/run_a_type/google/open_ended/question_3.txt: 909 tokens
         20_experiments/20_exp2/run_a_type/google/open_ended/question_1.txt: 670 tokens

================================================================================

[INFO] Overall Summary
[INFO] Total files processed: 372
[INFO] Total files truncated: 14 (3.8%)

[INFO] Truncated files sorted by token count:
         TRUNCATED 20_experiments/20_exp2/run_a_type/google/open_ended/question_3.txt: 909 tokens (177.54%)
         TRUNCATED 20_experiments/20_exp2/run_c_both/google/open_ended/question_4.txt: 872 tokens (170.31%)
         TRUNCATED 20_experiments/20_exp2/run_a_type/google/open_ended/question_5.txt: 823 tokens (160.74%)
         TRUNCATED 20_experiments/20_exp2/run_a_type/google/open_ended/question_2.txt: 819 tokens (159.96%)
         TRUNCATED 20_experiments/20_exp2/run_c_both/google/open_ended/question_6.txt: 691 tokens (134.96%)
         TRUNCATED 20_experiments/10_exp1/run_a_content/complex_prompt/google/transcript/layer4_question.txt: 676 tokens (132.03%)
         TRUNCATED 20_experiments/20_exp2/run_a_type/google/open_ended/question_6.txt: 674 tokens (131.64%)
         TRUNCATED 20_experiments/20_exp2/run_a_type/google/open_ended/question_1.txt: 670 tokens (130.86%)
         TRUNCATED 20_experiments/10_exp1/run_a_content/complex_prompt/google/transcript/layer7_question.txt: 652 tokens (127.34%)
         TRUNCATED 20_experiments/10_exp1/run_a_content/complex_prompt/google/tanenbaum/layer3_question.txt: 636 tokens (124.22%)
         TRUNCATED 20_experiments/20_exp2/run_b_bloom/deepseek/question_4.txt: 603 tokens (117.77%)
         TRUNCATED 20_experiments/20_exp2/run_b_bloom/google/question_4.txt: 571 tokens (111.52%)
         TRUNCATED 20_experiments/10_exp1/run_a_content/complex_prompt/google/tanenbaum/layer2_question.txt: 536 tokens (104.69%)
         TRUNCATED 20_experiments/20_exp2/run_c_both/deepseek/open_ended/question_4.txt: 534 tokens (104.30%)

Google: 12 times
DeepSeek: 2 times