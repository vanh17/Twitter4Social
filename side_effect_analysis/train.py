from BertLibrary import BertFTModel
import numpy as np

ft_model = BertFTModel( model_dir='sentiment140/uncased_L-12_H-768_A-12',
                         ckpt_name="bert_model.ckpt",
                         labels=['0','1'],
                         lr=5e-06,
                         num_train_steps=60000,
                         num_warmup_steps=1000,
                         ckpt_output_dir='sentiment140/output',
                         save_check_steps=1000,
                         do_lower_case=False,
                         max_seq_len=64,
                         batch_size=32,
                         )
ft_trainer =  ft_model.get_trainer()
ft_evaluator = ft_model.get_evaluator()

# training
ft_trainer.train_from_file('sentiment140', 60000)
ft_evaluator.evaluate_from_file('sentiment140', checkpoint="sentiment140/output/model.ckpt-60000") 