é°
Ŗż
8
Const
output"dtype"
valuetensor"
dtypetype

NoOp
C
Placeholder
output"dtype"
dtypetype"
shapeshape:
@
ReadVariableOp
resource
value"dtype"
dtypetype
¾
StatefulPartitionedCall
args2Tin
output2Tout"
Tin
list(type)("
Tout
list(type)("	
ffunc"
configstring "
config_protostring "
executor_typestring 
q
VarHandleOp
resource"
	containerstring "
shared_namestring "
dtypetype"
shapeshape"serve*2.2.02v2.2.0-rc4-8-g2b96f3662b8ę
t
dense/kernelVarHandleOp*
_output_shapes
: *
dtype0*
shape
:*
shared_namedense/kernel
m
 dense/kernel/Read/ReadVariableOpReadVariableOpdense/kernel*
_output_shapes

:*
dtype0
l

dense/biasVarHandleOp*
_output_shapes
: *
dtype0*
shape:*
shared_name
dense/bias
e
dense/bias/Read/ReadVariableOpReadVariableOp
dense/bias*
_output_shapes
:*
dtype0
d
SGD/iterVarHandleOp*
_output_shapes
: *
dtype0	*
shape: *
shared_name
SGD/iter
]
SGD/iter/Read/ReadVariableOpReadVariableOpSGD/iter*
_output_shapes
: *
dtype0	
f
	SGD/decayVarHandleOp*
_output_shapes
: *
dtype0*
shape: *
shared_name	SGD/decay
_
SGD/decay/Read/ReadVariableOpReadVariableOp	SGD/decay*
_output_shapes
: *
dtype0
v
SGD/learning_rateVarHandleOp*
_output_shapes
: *
dtype0*
shape: *"
shared_nameSGD/learning_rate
o
%SGD/learning_rate/Read/ReadVariableOpReadVariableOpSGD/learning_rate*
_output_shapes
: *
dtype0
l
SGD/momentumVarHandleOp*
_output_shapes
: *
dtype0*
shape: *
shared_nameSGD/momentum
e
 SGD/momentum/Read/ReadVariableOpReadVariableOpSGD/momentum*
_output_shapes
: *
dtype0
^
totalVarHandleOp*
_output_shapes
: *
dtype0*
shape: *
shared_nametotal
W
total/Read/ReadVariableOpReadVariableOptotal*
_output_shapes
: *
dtype0
^
countVarHandleOp*
_output_shapes
: *
dtype0*
shape: *
shared_namecount
W
count/Read/ReadVariableOpReadVariableOpcount*
_output_shapes
: *
dtype0

NoOpNoOp
Ē
ConstConst"/device:CPU:0*
_output_shapes
: *
dtype0*
valueųBõ Bī

layer_with_weights-0
layer-0
	optimizer
trainable_variables
regularization_losses
	variables
	keras_api

signatures
h

kernel
	bias

trainable_variables
regularization_losses
	variables
	keras_api
6
iter
	decay
learning_rate
momentum

0
	1
 

0
	1
­
trainable_variables
non_trainable_variables
layer_metrics
metrics

layers
layer_regularization_losses
regularization_losses
	variables
 
XV
VARIABLE_VALUEdense/kernel6layer_with_weights-0/kernel/.ATTRIBUTES/VARIABLE_VALUE
TR
VARIABLE_VALUE
dense/bias4layer_with_weights-0/bias/.ATTRIBUTES/VARIABLE_VALUE

0
	1
 

0
	1
­

trainable_variables
non_trainable_variables
metrics

layers
layer_regularization_losses
regularization_losses
	variables
layer_metrics
GE
VARIABLE_VALUESGD/iter)optimizer/iter/.ATTRIBUTES/VARIABLE_VALUE
IG
VARIABLE_VALUE	SGD/decay*optimizer/decay/.ATTRIBUTES/VARIABLE_VALUE
YW
VARIABLE_VALUESGD/learning_rate2optimizer/learning_rate/.ATTRIBUTES/VARIABLE_VALUE
OM
VARIABLE_VALUESGD/momentum-optimizer/momentum/.ATTRIBUTES/VARIABLE_VALUE
 
 

0

0
 
 
 
 
 
 
4
	total
	count
	variables
 	keras_api
OM
VARIABLE_VALUEtotal4keras_api/metrics/0/total/.ATTRIBUTES/VARIABLE_VALUE
OM
VARIABLE_VALUEcount4keras_api/metrics/0/count/.ATTRIBUTES/VARIABLE_VALUE

0
1

	variables
~
serving_default_dense_inputPlaceholder*'
_output_shapes
:’’’’’’’’’*
dtype0*
shape:’’’’’’’’’
Æ
StatefulPartitionedCallStatefulPartitionedCallserving_default_dense_inputdense/kernel
dense/bias*
Tin
2*
Tout
2*'
_output_shapes
:’’’’’’’’’*$
_read_only_resource_inputs
**
config_proto

CPU

GPU 2J 8**
f%R#
!__inference_signature_wrapper_833
O
saver_filenamePlaceholder*
_output_shapes
: *
dtype0*
shape: 
ü
StatefulPartitionedCall_1StatefulPartitionedCallsaver_filename dense/kernel/Read/ReadVariableOpdense/bias/Read/ReadVariableOpSGD/iter/Read/ReadVariableOpSGD/decay/Read/ReadVariableOp%SGD/learning_rate/Read/ReadVariableOp SGD/momentum/Read/ReadVariableOptotal/Read/ReadVariableOpcount/Read/ReadVariableOpConst*
Tin
2
	*
Tout
2*
_output_shapes
: * 
_read_only_resource_inputs
 **
config_proto

CPU

GPU 2J 8*%
f R
__inference__traced_save_941
×
StatefulPartitionedCall_2StatefulPartitionedCallsaver_filenamedense/kernel
dense/biasSGD/iter	SGD/decaySGD/learning_rateSGD/momentumtotalcount*
Tin
2	*
Tout
2*
_output_shapes
: * 
_read_only_resource_inputs
 **
config_proto

CPU

GPU 2J 8*(
f#R!
__inference__traced_restore_977äĮ
ź
x
#__inference_dense_layer_call_fn_890

inputs
unknown
	unknown_0
identity¢StatefulPartitionedCallĢ
StatefulPartitionedCallStatefulPartitionedCallinputsunknown	unknown_0*
Tin
2*
Tout
2*'
_output_shapes
:’’’’’’’’’*$
_read_only_resource_inputs
**
config_proto

CPU

GPU 2J 8*G
fBR@
>__inference_dense_layer_call_and_return_conditional_losses_7532
StatefulPartitionedCall
IdentityIdentity StatefulPartitionedCall:output:0^StatefulPartitionedCall*
T0*'
_output_shapes
:’’’’’’’’’2

Identity"
identityIdentity:output:0*.
_input_shapes
:’’’’’’’’’::22
StatefulPartitionedCallStatefulPartitionedCall:O K
'
_output_shapes
:’’’’’’’’’
 
_user_specified_nameinputs:

_output_shapes
: :

_output_shapes
: 
Č
„
C__inference_sequential_layer_call_and_return_conditional_losses_779
dense_input
	dense_773
	dense_775
identity¢dense/StatefulPartitionedCallß
dense/StatefulPartitionedCallStatefulPartitionedCalldense_input	dense_773	dense_775*
Tin
2*
Tout
2*'
_output_shapes
:’’’’’’’’’*$
_read_only_resource_inputs
**
config_proto

CPU

GPU 2J 8*G
fBR@
>__inference_dense_layer_call_and_return_conditional_losses_7532
dense/StatefulPartitionedCall
IdentityIdentity&dense/StatefulPartitionedCall:output:0^dense/StatefulPartitionedCall*
T0*'
_output_shapes
:’’’’’’’’’2

Identity"
identityIdentity:output:0*.
_input_shapes
:’’’’’’’’’::2>
dense/StatefulPartitionedCalldense/StatefulPartitionedCall:T P
'
_output_shapes
:’’’’’’’’’
%
_user_specified_namedense_input:

_output_shapes
: :

_output_shapes
: 
é
·
C__inference_sequential_layer_call_and_return_conditional_losses_843

inputs(
$dense_matmul_readvariableop_resource)
%dense_biasadd_readvariableop_resource
identity
dense/MatMul/ReadVariableOpReadVariableOp$dense_matmul_readvariableop_resource*
_output_shapes

:*
dtype02
dense/MatMul/ReadVariableOp
dense/MatMulMatMulinputs#dense/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:’’’’’’’’’2
dense/MatMul
dense/BiasAdd/ReadVariableOpReadVariableOp%dense_biasadd_readvariableop_resource*
_output_shapes
:*
dtype02
dense/BiasAdd/ReadVariableOp
dense/BiasAddBiasAdddense/MatMul:product:0$dense/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:’’’’’’’’’2
dense/BiasAddj
IdentityIdentitydense/BiasAdd:output:0*
T0*'
_output_shapes
:’’’’’’’’’2

Identity"
identityIdentity:output:0*.
_input_shapes
:’’’’’’’’’:::O K
'
_output_shapes
:’’’’’’’’’
 
_user_specified_nameinputs:

_output_shapes
: :

_output_shapes
: 


(__inference_sequential_layer_call_fn_816
dense_input
unknown
	unknown_0
identity¢StatefulPartitionedCallÖ
StatefulPartitionedCallStatefulPartitionedCalldense_inputunknown	unknown_0*
Tin
2*
Tout
2*'
_output_shapes
:’’’’’’’’’*$
_read_only_resource_inputs
**
config_proto

CPU

GPU 2J 8*L
fGRE
C__inference_sequential_layer_call_and_return_conditional_losses_8092
StatefulPartitionedCall
IdentityIdentity StatefulPartitionedCall:output:0^StatefulPartitionedCall*
T0*'
_output_shapes
:’’’’’’’’’2

Identity"
identityIdentity:output:0*.
_input_shapes
:’’’’’’’’’::22
StatefulPartitionedCallStatefulPartitionedCall:T P
'
_output_shapes
:’’’’’’’’’
%
_user_specified_namedense_input:

_output_shapes
: :

_output_shapes
: 
Ę)

__inference__traced_restore_977
file_prefix!
assignvariableop_dense_kernel!
assignvariableop_1_dense_bias
assignvariableop_2_sgd_iter 
assignvariableop_3_sgd_decay(
$assignvariableop_4_sgd_learning_rate#
assignvariableop_5_sgd_momentum
assignvariableop_6_total
assignvariableop_7_count

identity_9¢AssignVariableOp¢AssignVariableOp_1¢AssignVariableOp_2¢AssignVariableOp_3¢AssignVariableOp_4¢AssignVariableOp_5¢AssignVariableOp_6¢AssignVariableOp_7¢	RestoreV2¢RestoreV2_1
RestoreV2/tensor_namesConst"/device:CPU:0*
_output_shapes
:*
dtype0*©
valueBB6layer_with_weights-0/kernel/.ATTRIBUTES/VARIABLE_VALUEB4layer_with_weights-0/bias/.ATTRIBUTES/VARIABLE_VALUEB)optimizer/iter/.ATTRIBUTES/VARIABLE_VALUEB*optimizer/decay/.ATTRIBUTES/VARIABLE_VALUEB2optimizer/learning_rate/.ATTRIBUTES/VARIABLE_VALUEB-optimizer/momentum/.ATTRIBUTES/VARIABLE_VALUEB4keras_api/metrics/0/total/.ATTRIBUTES/VARIABLE_VALUEB4keras_api/metrics/0/count/.ATTRIBUTES/VARIABLE_VALUE2
RestoreV2/tensor_names
RestoreV2/shape_and_slicesConst"/device:CPU:0*
_output_shapes
:*
dtype0*#
valueBB B B B B B B B 2
RestoreV2/shape_and_slicesÓ
	RestoreV2	RestoreV2file_prefixRestoreV2/tensor_names:output:0#RestoreV2/shape_and_slices:output:0"/device:CPU:0*4
_output_shapes"
 ::::::::*
dtypes

2	2
	RestoreV2X
IdentityIdentityRestoreV2:tensors:0*
T0*
_output_shapes
:2

Identity
AssignVariableOpAssignVariableOpassignvariableop_dense_kernelIdentity:output:0*
_output_shapes
 *
dtype02
AssignVariableOp\

Identity_1IdentityRestoreV2:tensors:1*
T0*
_output_shapes
:2

Identity_1
AssignVariableOp_1AssignVariableOpassignvariableop_1_dense_biasIdentity_1:output:0*
_output_shapes
 *
dtype02
AssignVariableOp_1\

Identity_2IdentityRestoreV2:tensors:2*
T0	*
_output_shapes
:2

Identity_2
AssignVariableOp_2AssignVariableOpassignvariableop_2_sgd_iterIdentity_2:output:0*
_output_shapes
 *
dtype0	2
AssignVariableOp_2\

Identity_3IdentityRestoreV2:tensors:3*
T0*
_output_shapes
:2

Identity_3
AssignVariableOp_3AssignVariableOpassignvariableop_3_sgd_decayIdentity_3:output:0*
_output_shapes
 *
dtype02
AssignVariableOp_3\

Identity_4IdentityRestoreV2:tensors:4*
T0*
_output_shapes
:2

Identity_4
AssignVariableOp_4AssignVariableOp$assignvariableop_4_sgd_learning_rateIdentity_4:output:0*
_output_shapes
 *
dtype02
AssignVariableOp_4\

Identity_5IdentityRestoreV2:tensors:5*
T0*
_output_shapes
:2

Identity_5
AssignVariableOp_5AssignVariableOpassignvariableop_5_sgd_momentumIdentity_5:output:0*
_output_shapes
 *
dtype02
AssignVariableOp_5\

Identity_6IdentityRestoreV2:tensors:6*
T0*
_output_shapes
:2

Identity_6
AssignVariableOp_6AssignVariableOpassignvariableop_6_totalIdentity_6:output:0*
_output_shapes
 *
dtype02
AssignVariableOp_6\

Identity_7IdentityRestoreV2:tensors:7*
T0*
_output_shapes
:2

Identity_7
AssignVariableOp_7AssignVariableOpassignvariableop_7_countIdentity_7:output:0*
_output_shapes
 *
dtype02
AssignVariableOp_7Ø
RestoreV2_1/tensor_namesConst"/device:CPU:0*
_output_shapes
:*
dtype0*1
value(B&B_CHECKPOINTABLE_OBJECT_GRAPH2
RestoreV2_1/tensor_names
RestoreV2_1/shape_and_slicesConst"/device:CPU:0*
_output_shapes
:*
dtype0*
valueB
B 2
RestoreV2_1/shape_and_slicesÄ
RestoreV2_1	RestoreV2file_prefix!RestoreV2_1/tensor_names:output:0%RestoreV2_1/shape_and_slices:output:0
^RestoreV2"/device:CPU:0*
_output_shapes
:*
dtypes
22
RestoreV2_19
NoOpNoOp"/device:CPU:0*
_output_shapes
 2
NoOp

Identity_8Identityfile_prefix^AssignVariableOp^AssignVariableOp_1^AssignVariableOp_2^AssignVariableOp_3^AssignVariableOp_4^AssignVariableOp_5^AssignVariableOp_6^AssignVariableOp_7^NoOp"/device:CPU:0*
T0*
_output_shapes
: 2

Identity_8

Identity_9IdentityIdentity_8:output:0^AssignVariableOp^AssignVariableOp_1^AssignVariableOp_2^AssignVariableOp_3^AssignVariableOp_4^AssignVariableOp_5^AssignVariableOp_6^AssignVariableOp_7
^RestoreV2^RestoreV2_1*
T0*
_output_shapes
: 2

Identity_9"!

identity_9Identity_9:output:0*5
_input_shapes$
": ::::::::2$
AssignVariableOpAssignVariableOp2(
AssignVariableOp_1AssignVariableOp_12(
AssignVariableOp_2AssignVariableOp_22(
AssignVariableOp_3AssignVariableOp_32(
AssignVariableOp_4AssignVariableOp_42(
AssignVariableOp_5AssignVariableOp_52(
AssignVariableOp_6AssignVariableOp_62(
AssignVariableOp_7AssignVariableOp_72
	RestoreV2	RestoreV22
RestoreV2_1RestoreV2_1:C ?

_output_shapes
: 
%
_user_specified_namefile_prefix:

_output_shapes
: :

_output_shapes
: :

_output_shapes
: :

_output_shapes
: :

_output_shapes
: :

_output_shapes
: :

_output_shapes
: :

_output_shapes
: 


­
__inference__wrapped_model_739
dense_input3
/sequential_dense_matmul_readvariableop_resource4
0sequential_dense_biasadd_readvariableop_resource
identityĄ
&sequential/dense/MatMul/ReadVariableOpReadVariableOp/sequential_dense_matmul_readvariableop_resource*
_output_shapes

:*
dtype02(
&sequential/dense/MatMul/ReadVariableOp«
sequential/dense/MatMulMatMuldense_input.sequential/dense/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:’’’’’’’’’2
sequential/dense/MatMulæ
'sequential/dense/BiasAdd/ReadVariableOpReadVariableOp0sequential_dense_biasadd_readvariableop_resource*
_output_shapes
:*
dtype02)
'sequential/dense/BiasAdd/ReadVariableOpÅ
sequential/dense/BiasAddBiasAdd!sequential/dense/MatMul:product:0/sequential/dense/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:’’’’’’’’’2
sequential/dense/BiasAddu
IdentityIdentity!sequential/dense/BiasAdd:output:0*
T0*'
_output_shapes
:’’’’’’’’’2

Identity"
identityIdentity:output:0*.
_input_shapes
:’’’’’’’’’:::T P
'
_output_shapes
:’’’’’’’’’
%
_user_specified_namedense_input:

_output_shapes
: :

_output_shapes
: 
ō
}
(__inference_sequential_layer_call_fn_871

inputs
unknown
	unknown_0
identity¢StatefulPartitionedCallŃ
StatefulPartitionedCallStatefulPartitionedCallinputsunknown	unknown_0*
Tin
2*
Tout
2*'
_output_shapes
:’’’’’’’’’*$
_read_only_resource_inputs
**
config_proto

CPU

GPU 2J 8*L
fGRE
C__inference_sequential_layer_call_and_return_conditional_losses_8092
StatefulPartitionedCall
IdentityIdentity StatefulPartitionedCall:output:0^StatefulPartitionedCall*
T0*'
_output_shapes
:’’’’’’’’’2

Identity"
identityIdentity:output:0*.
_input_shapes
:’’’’’’’’’::22
StatefulPartitionedCallStatefulPartitionedCall:O K
'
_output_shapes
:’’’’’’’’’
 
_user_specified_nameinputs:

_output_shapes
: :

_output_shapes
: 
¹
 
C__inference_sequential_layer_call_and_return_conditional_losses_791

inputs
	dense_785
	dense_787
identity¢dense/StatefulPartitionedCallŚ
dense/StatefulPartitionedCallStatefulPartitionedCallinputs	dense_785	dense_787*
Tin
2*
Tout
2*'
_output_shapes
:’’’’’’’’’*$
_read_only_resource_inputs
**
config_proto

CPU

GPU 2J 8*G
fBR@
>__inference_dense_layer_call_and_return_conditional_losses_7532
dense/StatefulPartitionedCall
IdentityIdentity&dense/StatefulPartitionedCall:output:0^dense/StatefulPartitionedCall*
T0*'
_output_shapes
:’’’’’’’’’2

Identity"
identityIdentity:output:0*.
_input_shapes
:’’’’’’’’’::2>
dense/StatefulPartitionedCalldense/StatefulPartitionedCall:O K
'
_output_shapes
:’’’’’’’’’
 
_user_specified_nameinputs:

_output_shapes
: :

_output_shapes
: 
¹
 
C__inference_sequential_layer_call_and_return_conditional_losses_809

inputs
	dense_803
	dense_805
identity¢dense/StatefulPartitionedCallŚ
dense/StatefulPartitionedCallStatefulPartitionedCallinputs	dense_803	dense_805*
Tin
2*
Tout
2*'
_output_shapes
:’’’’’’’’’*$
_read_only_resource_inputs
**
config_proto

CPU

GPU 2J 8*G
fBR@
>__inference_dense_layer_call_and_return_conditional_losses_7532
dense/StatefulPartitionedCall
IdentityIdentity&dense/StatefulPartitionedCall:output:0^dense/StatefulPartitionedCall*
T0*'
_output_shapes
:’’’’’’’’’2

Identity"
identityIdentity:output:0*.
_input_shapes
:’’’’’’’’’::2>
dense/StatefulPartitionedCalldense/StatefulPartitionedCall:O K
'
_output_shapes
:’’’’’’’’’
 
_user_specified_nameinputs:

_output_shapes
: :

_output_shapes
: 

¦
>__inference_dense_layer_call_and_return_conditional_losses_753

inputs"
matmul_readvariableop_resource#
biasadd_readvariableop_resource
identity
MatMul/ReadVariableOpReadVariableOpmatmul_readvariableop_resource*
_output_shapes

:*
dtype02
MatMul/ReadVariableOps
MatMulMatMulinputsMatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:’’’’’’’’’2
MatMul
BiasAdd/ReadVariableOpReadVariableOpbiasadd_readvariableop_resource*
_output_shapes
:*
dtype02
BiasAdd/ReadVariableOp
BiasAddBiasAddMatMul:product:0BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:’’’’’’’’’2	
BiasAddd
IdentityIdentityBiasAdd:output:0*
T0*'
_output_shapes
:’’’’’’’’’2

Identity"
identityIdentity:output:0*.
_input_shapes
:’’’’’’’’’:::O K
'
_output_shapes
:’’’’’’’’’
 
_user_specified_nameinputs:

_output_shapes
: :

_output_shapes
: 
Ż$
Õ
__inference__traced_save_941
file_prefix+
'savev2_dense_kernel_read_readvariableop)
%savev2_dense_bias_read_readvariableop'
#savev2_sgd_iter_read_readvariableop	(
$savev2_sgd_decay_read_readvariableop0
,savev2_sgd_learning_rate_read_readvariableop+
'savev2_sgd_momentum_read_readvariableop$
 savev2_total_read_readvariableop$
 savev2_count_read_readvariableop
savev2_1_const

identity_1¢MergeV2Checkpoints¢SaveV2¢SaveV2_1
StaticRegexFullMatchStaticRegexFullMatchfile_prefix"/device:CPU:**
_output_shapes
: *
pattern
^s3://.*2
StaticRegexFullMatchc
ConstConst"/device:CPU:**
_output_shapes
: *
dtype0*
valueB B.part2
Const
Const_1Const"/device:CPU:**
_output_shapes
: *
dtype0*<
value3B1 B+_temp_08b469b61f60471b9bf062157ea2b3c9/part2	
Const_1
SelectSelectStaticRegexFullMatch:output:0Const:output:0Const_1:output:0"/device:CPU:**
T0*
_output_shapes
: 2
Selectt

StringJoin
StringJoinfile_prefixSelect:output:0"/device:CPU:**
N*
_output_shapes
: 2

StringJoinZ

num_shardsConst*
_output_shapes
: *
dtype0*
value	B :2

num_shards
ShardedFilename/shardConst"/device:CPU:0*
_output_shapes
: *
dtype0*
value	B : 2
ShardedFilename/shard¦
ShardedFilenameShardedFilenameStringJoin:output:0ShardedFilename/shard:output:0num_shards:output:0"/device:CPU:0*
_output_shapes
: 2
ShardedFilename
SaveV2/tensor_namesConst"/device:CPU:0*
_output_shapes
:*
dtype0*©
valueBB6layer_with_weights-0/kernel/.ATTRIBUTES/VARIABLE_VALUEB4layer_with_weights-0/bias/.ATTRIBUTES/VARIABLE_VALUEB)optimizer/iter/.ATTRIBUTES/VARIABLE_VALUEB*optimizer/decay/.ATTRIBUTES/VARIABLE_VALUEB2optimizer/learning_rate/.ATTRIBUTES/VARIABLE_VALUEB-optimizer/momentum/.ATTRIBUTES/VARIABLE_VALUEB4keras_api/metrics/0/total/.ATTRIBUTES/VARIABLE_VALUEB4keras_api/metrics/0/count/.ATTRIBUTES/VARIABLE_VALUE2
SaveV2/tensor_names
SaveV2/shape_and_slicesConst"/device:CPU:0*
_output_shapes
:*
dtype0*#
valueBB B B B B B B B 2
SaveV2/shape_and_slicesé
SaveV2SaveV2ShardedFilename:filename:0SaveV2/tensor_names:output:0 SaveV2/shape_and_slices:output:0'savev2_dense_kernel_read_readvariableop%savev2_dense_bias_read_readvariableop#savev2_sgd_iter_read_readvariableop$savev2_sgd_decay_read_readvariableop,savev2_sgd_learning_rate_read_readvariableop'savev2_sgd_momentum_read_readvariableop savev2_total_read_readvariableop savev2_count_read_readvariableop"/device:CPU:0*
_output_shapes
 *
dtypes

2	2
SaveV2
ShardedFilename_1/shardConst"/device:CPU:0*
_output_shapes
: *
dtype0*
value	B :2
ShardedFilename_1/shard¬
ShardedFilename_1ShardedFilenameStringJoin:output:0 ShardedFilename_1/shard:output:0num_shards:output:0"/device:CPU:0*
_output_shapes
: 2
ShardedFilename_1¢
SaveV2_1/tensor_namesConst"/device:CPU:0*
_output_shapes
:*
dtype0*1
value(B&B_CHECKPOINTABLE_OBJECT_GRAPH2
SaveV2_1/tensor_names
SaveV2_1/shape_and_slicesConst"/device:CPU:0*
_output_shapes
:*
dtype0*
valueB
B 2
SaveV2_1/shape_and_slicesĻ
SaveV2_1SaveV2ShardedFilename_1:filename:0SaveV2_1/tensor_names:output:0"SaveV2_1/shape_and_slices:output:0savev2_1_const^SaveV2"/device:CPU:0*
_output_shapes
 *
dtypes
22

SaveV2_1ć
&MergeV2Checkpoints/checkpoint_prefixesPackShardedFilename:filename:0ShardedFilename_1:filename:0^SaveV2	^SaveV2_1"/device:CPU:0*
N*
T0*
_output_shapes
:2(
&MergeV2Checkpoints/checkpoint_prefixes¬
MergeV2CheckpointsMergeV2Checkpoints/MergeV2Checkpoints/checkpoint_prefixes:output:0file_prefix	^SaveV2_1"/device:CPU:0*
_output_shapes
 2
MergeV2Checkpointsr
IdentityIdentityfile_prefix^MergeV2Checkpoints"/device:CPU:0*
T0*
_output_shapes
: 2

Identity

Identity_1IdentityIdentity:output:0^MergeV2Checkpoints^SaveV2	^SaveV2_1*
T0*
_output_shapes
: 2

Identity_1"!

identity_1Identity_1:output:0*3
_input_shapes"
 : ::: : : : : : : 2(
MergeV2CheckpointsMergeV2Checkpoints2
SaveV2SaveV22
SaveV2_1SaveV2_1:C ?

_output_shapes
: 
%
_user_specified_namefile_prefix:$ 

_output_shapes

:: 

_output_shapes
::

_output_shapes
: :

_output_shapes
: :

_output_shapes
: :

_output_shapes
: :

_output_shapes
: :

_output_shapes
: :	

_output_shapes
: 

¦
>__inference_dense_layer_call_and_return_conditional_losses_881

inputs"
matmul_readvariableop_resource#
biasadd_readvariableop_resource
identity
MatMul/ReadVariableOpReadVariableOpmatmul_readvariableop_resource*
_output_shapes

:*
dtype02
MatMul/ReadVariableOps
MatMulMatMulinputsMatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:’’’’’’’’’2
MatMul
BiasAdd/ReadVariableOpReadVariableOpbiasadd_readvariableop_resource*
_output_shapes
:*
dtype02
BiasAdd/ReadVariableOp
BiasAddBiasAddMatMul:product:0BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:’’’’’’’’’2	
BiasAddd
IdentityIdentityBiasAdd:output:0*
T0*'
_output_shapes
:’’’’’’’’’2

Identity"
identityIdentity:output:0*.
_input_shapes
:’’’’’’’’’:::O K
'
_output_shapes
:’’’’’’’’’
 
_user_specified_nameinputs:

_output_shapes
: :

_output_shapes
: 
ō
}
(__inference_sequential_layer_call_fn_862

inputs
unknown
	unknown_0
identity¢StatefulPartitionedCallŃ
StatefulPartitionedCallStatefulPartitionedCallinputsunknown	unknown_0*
Tin
2*
Tout
2*'
_output_shapes
:’’’’’’’’’*$
_read_only_resource_inputs
**
config_proto

CPU

GPU 2J 8*L
fGRE
C__inference_sequential_layer_call_and_return_conditional_losses_7912
StatefulPartitionedCall
IdentityIdentity StatefulPartitionedCall:output:0^StatefulPartitionedCall*
T0*'
_output_shapes
:’’’’’’’’’2

Identity"
identityIdentity:output:0*.
_input_shapes
:’’’’’’’’’::22
StatefulPartitionedCallStatefulPartitionedCall:O K
'
_output_shapes
:’’’’’’’’’
 
_user_specified_nameinputs:

_output_shapes
: :

_output_shapes
: 
Č
„
C__inference_sequential_layer_call_and_return_conditional_losses_770
dense_input
	dense_764
	dense_766
identity¢dense/StatefulPartitionedCallß
dense/StatefulPartitionedCallStatefulPartitionedCalldense_input	dense_764	dense_766*
Tin
2*
Tout
2*'
_output_shapes
:’’’’’’’’’*$
_read_only_resource_inputs
**
config_proto

CPU

GPU 2J 8*G
fBR@
>__inference_dense_layer_call_and_return_conditional_losses_7532
dense/StatefulPartitionedCall
IdentityIdentity&dense/StatefulPartitionedCall:output:0^dense/StatefulPartitionedCall*
T0*'
_output_shapes
:’’’’’’’’’2

Identity"
identityIdentity:output:0*.
_input_shapes
:’’’’’’’’’::2>
dense/StatefulPartitionedCalldense/StatefulPartitionedCall:T P
'
_output_shapes
:’’’’’’’’’
%
_user_specified_namedense_input:

_output_shapes
: :

_output_shapes
: 
é
·
C__inference_sequential_layer_call_and_return_conditional_losses_853

inputs(
$dense_matmul_readvariableop_resource)
%dense_biasadd_readvariableop_resource
identity
dense/MatMul/ReadVariableOpReadVariableOp$dense_matmul_readvariableop_resource*
_output_shapes

:*
dtype02
dense/MatMul/ReadVariableOp
dense/MatMulMatMulinputs#dense/MatMul/ReadVariableOp:value:0*
T0*'
_output_shapes
:’’’’’’’’’2
dense/MatMul
dense/BiasAdd/ReadVariableOpReadVariableOp%dense_biasadd_readvariableop_resource*
_output_shapes
:*
dtype02
dense/BiasAdd/ReadVariableOp
dense/BiasAddBiasAdddense/MatMul:product:0$dense/BiasAdd/ReadVariableOp:value:0*
T0*'
_output_shapes
:’’’’’’’’’2
dense/BiasAddj
IdentityIdentitydense/BiasAdd:output:0*
T0*'
_output_shapes
:’’’’’’’’’2

Identity"
identityIdentity:output:0*.
_input_shapes
:’’’’’’’’’:::O K
'
_output_shapes
:’’’’’’’’’
 
_user_specified_nameinputs:

_output_shapes
: :

_output_shapes
: 


(__inference_sequential_layer_call_fn_798
dense_input
unknown
	unknown_0
identity¢StatefulPartitionedCallÖ
StatefulPartitionedCallStatefulPartitionedCalldense_inputunknown	unknown_0*
Tin
2*
Tout
2*'
_output_shapes
:’’’’’’’’’*$
_read_only_resource_inputs
**
config_proto

CPU

GPU 2J 8*L
fGRE
C__inference_sequential_layer_call_and_return_conditional_losses_7912
StatefulPartitionedCall
IdentityIdentity StatefulPartitionedCall:output:0^StatefulPartitionedCall*
T0*'
_output_shapes
:’’’’’’’’’2

Identity"
identityIdentity:output:0*.
_input_shapes
:’’’’’’’’’::22
StatefulPartitionedCallStatefulPartitionedCall:T P
'
_output_shapes
:’’’’’’’’’
%
_user_specified_namedense_input:

_output_shapes
: :

_output_shapes
: 
×
{
!__inference_signature_wrapper_833
dense_input
unknown
	unknown_0
identity¢StatefulPartitionedCall±
StatefulPartitionedCallStatefulPartitionedCalldense_inputunknown	unknown_0*
Tin
2*
Tout
2*'
_output_shapes
:’’’’’’’’’*$
_read_only_resource_inputs
**
config_proto

CPU

GPU 2J 8*'
f"R 
__inference__wrapped_model_7392
StatefulPartitionedCall
IdentityIdentity StatefulPartitionedCall:output:0^StatefulPartitionedCall*
T0*'
_output_shapes
:’’’’’’’’’2

Identity"
identityIdentity:output:0*.
_input_shapes
:’’’’’’’’’::22
StatefulPartitionedCallStatefulPartitionedCall:T P
'
_output_shapes
:’’’’’’’’’
%
_user_specified_namedense_input:

_output_shapes
: :

_output_shapes
: "ÆL
saver_filename:0StatefulPartitionedCall_1:0StatefulPartitionedCall_28"
saved_model_main_op

NoOp*>
__saved_model_init_op%#
__saved_model_init_op

NoOp*°
serving_default
C
dense_input4
serving_default_dense_input:0’’’’’’’’’9
dense0
StatefulPartitionedCall:0’’’’’’’’’tensorflow/serving/predict:øC
õ
layer_with_weights-0
layer-0
	optimizer
trainable_variables
regularization_losses
	variables
	keras_api

signatures
*!&call_and_return_all_conditional_losses
"_default_save_signature
#__call__"
_tf_keras_sequentialä{"class_name": "Sequential", "name": "sequential", "trainable": true, "expects_training_arg": true, "dtype": "float32", "batch_input_shape": null, "config": {"name": "sequential", "layers": [{"class_name": "Dense", "config": {"name": "dense", "trainable": true, "batch_input_shape": {"class_name": "__tuple__", "items": [null, 1]}, "dtype": "float32", "units": 1, "activation": "linear", "use_bias": true, "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}}], "build_input_shape": {"class_name": "TensorShape", "items": [null, 1]}}, "input_spec": {"class_name": "InputSpec", "config": {"dtype": null, "shape": null, "ndim": null, "max_ndim": null, "min_ndim": 2, "axes": {"-1": 1}}}, "build_input_shape": {"class_name": "TensorShape", "items": [null, 1]}, "is_graph_network": true, "keras_version": "2.3.0-tf", "backend": "tensorflow", "model_config": {"class_name": "Sequential", "config": {"name": "sequential", "layers": [{"class_name": "Dense", "config": {"name": "dense", "trainable": true, "batch_input_shape": {"class_name": "__tuple__", "items": [null, 1]}, "dtype": "float32", "units": 1, "activation": "linear", "use_bias": true, "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}}], "build_input_shape": {"class_name": "TensorShape", "items": [null, 1]}}}, "training_config": {"loss": "mean_squared_error", "metrics": null, "weighted_metrics": null, "loss_weights": null, "sample_weight_mode": null, "optimizer_config": {"class_name": "SGD", "config": {"name": "SGD", "learning_rate": 0.009999999776482582, "decay": 0.0, "momentum": 0.0, "nesterov": false}}}}
¹

kernel
	bias

trainable_variables
regularization_losses
	variables
	keras_api
*$&call_and_return_all_conditional_losses
%__call__"
_tf_keras_layerś{"class_name": "Dense", "name": "dense", "trainable": true, "expects_training_arg": false, "dtype": "float32", "batch_input_shape": {"class_name": "__tuple__", "items": [null, 1]}, "stateful": false, "config": {"name": "dense", "trainable": true, "batch_input_shape": {"class_name": "__tuple__", "items": [null, 1]}, "dtype": "float32", "units": 1, "activation": "linear", "use_bias": true, "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}, "input_spec": {"class_name": "InputSpec", "config": {"dtype": null, "shape": null, "ndim": null, "max_ndim": null, "min_ndim": 2, "axes": {"-1": 1}}}, "build_input_shape": {"class_name": "TensorShape", "items": [null, 1]}}
I
iter
	decay
learning_rate
momentum"
	optimizer
.
0
	1"
trackable_list_wrapper
 "
trackable_list_wrapper
.
0
	1"
trackable_list_wrapper
Ź
trainable_variables
non_trainable_variables
layer_metrics
metrics

layers
layer_regularization_losses
regularization_losses
	variables
#__call__
"_default_save_signature
*!&call_and_return_all_conditional_losses
&!"call_and_return_conditional_losses"
_generic_user_object
,
&serving_default"
signature_map
:2dense/kernel
:2
dense/bias
.
0
	1"
trackable_list_wrapper
 "
trackable_list_wrapper
.
0
	1"
trackable_list_wrapper
­

trainable_variables
non_trainable_variables
metrics

layers
layer_regularization_losses
regularization_losses
	variables
layer_metrics
%__call__
*$&call_and_return_all_conditional_losses
&$"call_and_return_conditional_losses"
_generic_user_object
:	 (2SGD/iter
: (2	SGD/decay
: (2SGD/learning_rate
: (2SGD/momentum
 "
trackable_list_wrapper
 "
trackable_dict_wrapper
'
0"
trackable_list_wrapper
'
0"
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_dict_wrapper
»
	total
	count
	variables
 	keras_api"
_tf_keras_metricj{"class_name": "Mean", "name": "loss", "dtype": "float32", "config": {"name": "loss", "dtype": "float32"}}
:  (2total
:  (2count
.
0
1"
trackable_list_wrapper
-
	variables"
_generic_user_object
Ś2×
C__inference_sequential_layer_call_and_return_conditional_losses_779
C__inference_sequential_layer_call_and_return_conditional_losses_843
C__inference_sequential_layer_call_and_return_conditional_losses_853
C__inference_sequential_layer_call_and_return_conditional_losses_770Ą
·²³
FullArgSpec1
args)&
jself
jinputs

jtraining
jmask
varargs
 
varkw
 
defaults
p 

 

kwonlyargs 
kwonlydefaultsŖ 
annotationsŖ *
 
ą2Ż
__inference__wrapped_model_739ŗ
²
FullArgSpec
args 
varargsjargs
varkw
 
defaults
 

kwonlyargs 
kwonlydefaults
 
annotationsŖ **¢'
%"
dense_input’’’’’’’’’
ī2ė
(__inference_sequential_layer_call_fn_798
(__inference_sequential_layer_call_fn_862
(__inference_sequential_layer_call_fn_871
(__inference_sequential_layer_call_fn_816Ą
·²³
FullArgSpec1
args)&
jself
jinputs

jtraining
jmask
varargs
 
varkw
 
defaults
p 

 

kwonlyargs 
kwonlydefaultsŖ 
annotationsŖ *
 
č2å
>__inference_dense_layer_call_and_return_conditional_losses_881¢
²
FullArgSpec
args
jself
jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs 
kwonlydefaults
 
annotationsŖ *
 
Ķ2Ź
#__inference_dense_layer_call_fn_890¢
²
FullArgSpec
args
jself
jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs 
kwonlydefaults
 
annotationsŖ *
 
4B2
!__inference_signature_wrapper_833dense_input
__inference__wrapped_model_739i	4¢1
*¢'
%"
dense_input’’’’’’’’’
Ŗ "-Ŗ*
(
dense
dense’’’’’’’’’
>__inference_dense_layer_call_and_return_conditional_losses_881\	/¢,
%¢"
 
inputs’’’’’’’’’
Ŗ "%¢"

0’’’’’’’’’
 v
#__inference_dense_layer_call_fn_890O	/¢,
%¢"
 
inputs’’’’’’’’’
Ŗ "’’’’’’’’’°
C__inference_sequential_layer_call_and_return_conditional_losses_770i	<¢9
2¢/
%"
dense_input’’’’’’’’’
p

 
Ŗ "%¢"

0’’’’’’’’’
 °
C__inference_sequential_layer_call_and_return_conditional_losses_779i	<¢9
2¢/
%"
dense_input’’’’’’’’’
p 

 
Ŗ "%¢"

0’’’’’’’’’
 «
C__inference_sequential_layer_call_and_return_conditional_losses_843d	7¢4
-¢*
 
inputs’’’’’’’’’
p

 
Ŗ "%¢"

0’’’’’’’’’
 «
C__inference_sequential_layer_call_and_return_conditional_losses_853d	7¢4
-¢*
 
inputs’’’’’’’’’
p 

 
Ŗ "%¢"

0’’’’’’’’’
 
(__inference_sequential_layer_call_fn_798\	<¢9
2¢/
%"
dense_input’’’’’’’’’
p

 
Ŗ "’’’’’’’’’
(__inference_sequential_layer_call_fn_816\	<¢9
2¢/
%"
dense_input’’’’’’’’’
p 

 
Ŗ "’’’’’’’’’
(__inference_sequential_layer_call_fn_862W	7¢4
-¢*
 
inputs’’’’’’’’’
p

 
Ŗ "’’’’’’’’’
(__inference_sequential_layer_call_fn_871W	7¢4
-¢*
 
inputs’’’’’’’’’
p 

 
Ŗ "’’’’’’’’’
!__inference_signature_wrapper_833x	C¢@
¢ 
9Ŗ6
4
dense_input%"
dense_input’’’’’’’’’"-Ŗ*
(
dense
dense’’’’’’’’’