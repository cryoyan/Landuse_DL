#!/usr/bin/env python
# Filename: export_graph.py 
"""
introduction: export the frozen inference graph (a pb file) for prediction

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 21 January, 2021
"""

import os, sys


def export_graph(export_script,CKPT_PATH,EXPORT_PATH,model_variant,num_of_classes,atrous_rates1,atrous_rates2,atrous_rates3,output_stride,
                 multi_scale):
    command_string = 'python ' \
                     + export_script \
                     + ' --logtostderr' \
                     + ' --checkpoint_path='+ CKPT_PATH \
                     + ' --export_path='+ EXPORT_PATH \
                     + ' --model_variant=' + model_variant \
                     + ' --num_classes=' + str(num_of_classes) \
                     + ' --atrous_rates=' + str(atrous_rates1) \
                     + ' --atrous_rates=' + str(atrous_rates2) \
                     + ' --atrous_rates=' + str(atrous_rates3) \
                     + ' --output_stride=' + str(output_stride) \
                     + ' --decoder_output_stride=4 ' \
                     + ' --crop_size=513' \
                     + ' --crop_size=513'

    if multi_scale == 1:
        command_string += ' --inference_scales=' + str(0.5) \
                          + ' --inference_scales=' + str(0.75) \
                          + ' --inference_scales=' + str(1.0) \
                          + ' --inference_scales=' + str(1.25) \
                          + ' --inference_scales=' + str(1.5) \
                          + ' --inference_scales=' + str(1.75)
    elif multi_scale == 0:
        command_string += ' --inference_scales=' + str(1.0)
    else:
        raise ValueError(' Wrong input of the multi_scale parameter, only 0 or 1')

    res = os.system(command_string)
    if res != 0:
        sys.exit(1)


if __name__ == '__main__':
    print("%s : export the frozen inference graph" % os.path.basename(sys.argv[0]))

    para_file = sys.argv[1]
    if os.path.isfile(para_file) is False:
        raise IOError('File %s not exists in current folder: %s' % (para_file, os.getcwd()))

    code_dir = os.path.join(os.path.dirname(sys.argv[0]), '..')
    sys.path.insert(0, code_dir)
    import parameters

    tf_research_dir = parameters.get_directory_None_if_absence(para_file,'tf_research_dir')
    print(tf_research_dir)
    if tf_research_dir is None:
        raise ValueError('tf_research_dir is not in %s'%para_file)
    if os.path.isdir(tf_research_dir) is False:
        raise ValueError('%s does not exist' % tf_research_dir)
    if os.getenv('PYTHONPATH'):
        os.environ['PYTHONPATH'] = os.getenv('PYTHONPATH') + ':' + tf_research_dir + ':' +os.path.join(tf_research_dir,'slim')
    else:
        os.environ['PYTHONPATH'] = tf_research_dir + ':' +os.path.join(tf_research_dir,'slim')

    deeplab_dir = os.path.join(tf_research_dir,'deeplab')
    WORK_DIR = os.getcwd()

    expr_name = parameters.get_string_parameters(para_file,'expr_name')
    network_setting_ini = parameters.get_string_parameters(para_file,'network_setting_ini')
    EXP_FOLDER = expr_name
    TRAIN_LOGDIR = os.path.join(WORK_DIR, EXP_FOLDER, 'train')
    EXPORT_DIR = os.path.join(WORK_DIR, EXP_FOLDER, 'export')

    output_stride = parameters.get_digit_parameters_None_if_absence(network_setting_ini,'output_stride','int')
    atrous_rates1 = parameters.get_digit_parameters_None_if_absence(network_setting_ini,'atrous_rates1','int')
    atrous_rates2 = parameters.get_digit_parameters_None_if_absence(network_setting_ini,'atrous_rates2','int')
    atrous_rates3 = parameters.get_digit_parameters_None_if_absence(network_setting_ini,'atrous_rates3','int')

    model_variant = parameters.get_string_parameters(network_setting_ini, 'model_variant')
    num_classes_noBG = parameters.get_digit_parameters_None_if_absence(para_file, 'NUM_CLASSES_noBG', 'int')
    assert num_classes_noBG != None
    num_of_classes = num_classes_noBG + 1

    #export iteration
    iteration_num = parameters.get_digit_parameters_None_if_absence(network_setting_ini, 'export_iteration_num', 'int')

    multi_scale = parameters.get_digit_parameters_None_if_absence(network_setting_ini,'export_multi_scale','int')

    export_script = os.path.join(deeplab_dir, 'export_model.py')
    CKPT_PATH = os.path.join(TRAIN_LOGDIR, 'model.ckpt-%s'%iteration_num)

    EXPORT_PATH = os.path.join(EXPORT_DIR, 'frozen_inference_graph_%s.pb'%iteration_num)
    export_graph(export_script,CKPT_PATH,EXPORT_PATH,model_variant,num_of_classes,
                 atrous_rates1, atrous_rates2, atrous_rates3,output_stride,multi_scale)