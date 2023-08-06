import json
import numpy as np
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from hitrustai_lab.matrix.model_performance import ModelPerfornance
# from hitrustai_lab.orm.Tables.ModelPerformance import Model_Performance

dict_init_arg = {
    "list_y_test": list,
    "list_y_score": np.array,
    "customer_id_lst": str,
    "training_id_lst": str,
    "model_id_lst": str,
    "profile_id_lst": str,
    "tag_lst": str,
    # "connector_id_lst": str,
    # "operator_id_lst": str,
    # "institute_id_lst": str,
    "model_name_lst": str,
    "training_start_time_lst": str,
    "total_training_time_lst": int,
    "training_start_time_lst": datetime,
    "training_end_time_lst": datetime,
    "number_of_dump_data": int,
    "number_of_training_data_lst": int,
    "number_of_positive_samples_in_training_data": int,
    "number_of_negative_samples_in_training_data": int,
    "number_of_validation_data": int,
    "true_label_column_lst": str,
    "number_of_positive_samples_in_validation_data": int,
    "number_of_negative_samples_in_validation_data": int,
}


class TrainModelToSQl:
    def __init__(self, dict_init_arg, host="192.168.10.102", port="3305", user="root", passwd="root16313302", db="diia_test") -> None:
        self.engine = create_engine(
            f"mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset=utf8mb4&binary_prefix=true",
            echo=False
        )
        self.dict_init_arg = dict_init_arg

    def performance(self):
        mp = ModelPerfornance(score_type='policy_score')
        result = mp.performance_output(
            self.dict_init_arg["list_y_test"], self.dict_init_arg["list_y_score"])

        result = {
            'customer_id': self.dict_init_arg["customer_id_lst"],
            'training_id': self.dict_init_arg["training_id_lst"],
            'model_id': self.dict_init_arg["model_id_lst"],
            'profile_id': self.dict_init_arg["profile_id_lst"],
            'tag': self.dict_init_arg["tag_lst"],
            # 'connector_id': self.dict_init_arg["connector_id_lst"],
            # 'institute_id': self.dict_init_arg["institute_id_lst"],
            # 'operator_id': self.dict_init_arg["operator_id_lst"],
            'model_name': self.dict_init_arg["model_name_lst"],
            'training_start_time': self.dict_init_arg["training_start_time_lst"],
            'training_end_time': self.dict_init_arg["training_end_time_lst"],
            'total_training_time': self.dict_init_arg["total_training_time_lst"],
            'training_data_start_date': self.dict_init_arg["training_start_time_lst"],
            'training_data_end_date': self.dict_init_arg["training_end_time_lst"],
            'number_of_dump_data': self.dict_init_arg["number_of_dump_data"],
            'number_of_training_data': self.dict_init_arg["number_of_training_data_lst"],
            'number_of_positive_samples_in_training_data': self.dict_init_arg["number_of_positive_samples_in_training_data"],
            'number_of_negative_samples_in_training_data': self.dict_init_arg["number_of_negative_samples_in_training_data"],
            'number_of_validation_data': self.dict_init_arg["number_of_validation_data"],
            'true_label_column': self.dict_init_arg["true_label_column_lst"],
            'number_of_positive_samples_in_validation_data': self.dict_init_arg["number_of_positive_samples_in_validation_data"],
            'number_of_negative_samples_in_validation_data': self.dict_init_arg["number_of_negative_samples_in_validation_data"],
            'threshold': [result['threshold_lst']],
            'tp': [result['tp_lst']],
            'fp': [result['fp_lst']],
            'tn': [result['tn_lst']],
            'fn': [result['fn_lst']],
            'accuracy': [result['accuracy_lst']],
            'ppv': [result['precision_lst']],
            'recall': [result['recall_lst']],
            'f1_score': [result['f1_score_lst']],
            'fnr': [result['fnr_lst']],
            'fpr': [result['fpr_lst']],
            'npv': [result['npv_lst']],
            'fdr': [result['fdr_lst']],
            'for_': [result['for_lst']],
            'tnr': [result['tnr_lst']],
            'auc': result['auc_lst'],
        }
        return result

    def dict_to_dataframe(self):
        df = pd.DataFrame(data=self.performance())
        df['total_training_time'] = df.total_training_time
        df['training_data_start_date'] = df.training_data_start_date
        df['training_data_end_date'] = df.training_data_end_date

        for col in [
            'threshold', 'tp', 'fp', 'tn', 'fn', 'accuracy', 'ppv', 'recall', 'f1_score',
            'fnr', 'fpr', 'npv', 'fdr', 'for_', 'tnr'
        ]:
            df[col] = df[col].apply(lambda x: json.dumps(x))

        return df

    def insert_db(self, table):
        df = self.dict_to_dataframe()

        Session = sessionmaker(bind=self.engine)
        try:
            session = Session()
            session.bulk_insert_mappings(table, df.to_dict(orient='records'))
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
        finally:
            session.close()


if __name__ == '__main__':
    tmts = TrainModelToSQl(
        dict_init_arg,
        host="192.168.10.102",
        port="3305",
        user="root",
        passwd="root16313302",
        db="diia_test"
    )
    tmts.insert_db()
