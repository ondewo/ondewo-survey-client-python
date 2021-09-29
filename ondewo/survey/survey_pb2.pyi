# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
)

from google.protobuf.field_mask_pb2 import (
    FieldMask as google___protobuf___field_mask_pb2___FieldMask,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
    RepeatedScalarFieldContainer as google___protobuf___internal___containers___RepeatedScalarFieldContainer,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from typing import (
    Iterable as typing___Iterable,
    List as typing___List,
    Optional as typing___Optional,
    Text as typing___Text,
    Tuple as typing___Tuple,
    Union as typing___Union,
    cast as typing___cast,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int
builtin___str = str
if sys.version_info < (3,):
    builtin___buffer = buffer
    builtin___unicode = unicode


class SubFlow(builtin___int):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    @classmethod
    def Name(cls, number: builtin___int) -> builtin___str: ...
    @classmethod
    def Value(cls, name: builtin___str) -> 'SubFlow': ...
    @classmethod
    def keys(cls) -> typing___List[builtin___str]: ...
    @classmethod
    def values(cls) -> typing___List['SubFlow']: ...
    @classmethod
    def items(cls) -> typing___List[typing___Tuple[builtin___str, 'SubFlow']]: ...
    SUBFLOW_UNSPECIFIED = typing___cast('SubFlow', 0)
    BOT = typing___cast('SubFlow', 1)
    LEGAL_ENTITY = typing___cast('SubFlow', 2)
    POSTAL_ADDRESS = typing___cast('SubFlow', 3)
    EMAIL_ADDRESS = typing___cast('SubFlow', 4)
    PHONE_NUMBER = typing___cast('SubFlow', 5)
    PHONE_HOURS = typing___cast('SubFlow', 6)
    EXPECTED_DURATION = typing___cast('SubFlow', 7)
    PURPOSE = typing___cast('SubFlow', 8)
SUBFLOW_UNSPECIFIED = typing___cast('SubFlow', 0)
BOT = typing___cast('SubFlow', 1)
LEGAL_ENTITY = typing___cast('SubFlow', 2)
POSTAL_ADDRESS = typing___cast('SubFlow', 3)
EMAIL_ADDRESS = typing___cast('SubFlow', 4)
PHONE_NUMBER = typing___cast('SubFlow', 5)
PHONE_HOURS = typing___cast('SubFlow', 6)
EXPECTED_DURATION = typing___cast('SubFlow', 7)
PURPOSE = typing___cast('SubFlow', 8)
global___SubFlow = SubFlow

class Survey(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class AgentStatus(builtin___int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: builtin___int) -> builtin___str: ...
        @classmethod
        def Value(cls, name: builtin___str) -> 'Survey.AgentStatus': ...
        @classmethod
        def keys(cls) -> typing___List[builtin___str]: ...
        @classmethod
        def values(cls) -> typing___List['Survey.AgentStatus']: ...
        @classmethod
        def items(cls) -> typing___List[typing___Tuple[builtin___str, 'Survey.AgentStatus']]: ...
        TO_BE_INITIALIZED = typing___cast('Survey.AgentStatus', 0)
        UPDATED = typing___cast('Survey.AgentStatus', 1)
        UPDATING = typing___cast('Survey.AgentStatus', 2)
        OUTDATED = typing___cast('Survey.AgentStatus', 3)
    TO_BE_INITIALIZED = typing___cast('Survey.AgentStatus', 0)
    UPDATED = typing___cast('Survey.AgentStatus', 1)
    UPDATING = typing___cast('Survey.AgentStatus', 2)
    OUTDATED = typing___cast('Survey.AgentStatus', 3)
    global___AgentStatus = AgentStatus

    survey_id = ... # type: typing___Text
    display_name = ... # type: typing___Text
    language_code = ... # type: typing___Text
    exclude_subflows = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[global___SubFlow]
    status = ... # type: global___Survey.AgentStatus

    @property
    def questions(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[global___Question]: ...

    @property
    def survey_info(self) -> global___SurveyInfo: ...

    def __init__(self,
        *,
        survey_id : typing___Optional[typing___Text] = None,
        display_name : typing___Optional[typing___Text] = None,
        language_code : typing___Optional[typing___Text] = None,
        questions : typing___Optional[typing___Iterable[global___Question]] = None,
        survey_info : typing___Optional[global___SurveyInfo] = None,
        exclude_subflows : typing___Optional[typing___Iterable[global___SubFlow]] = None,
        status : typing___Optional[global___Survey.AgentStatus] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> Survey: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> Survey: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"survey_info",b"survey_info"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"display_name",b"display_name",u"exclude_subflows",b"exclude_subflows",u"language_code",b"language_code",u"questions",b"questions",u"status",b"status",u"survey_id",b"survey_id",u"survey_info",b"survey_info"]) -> None: ...
global___Survey = Survey

class SurveyInfo(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    legal_entity = ... # type: typing___Text
    postal_address = ... # type: typing___Text
    email_address = ... # type: typing___Text
    phone_number = ... # type: typing___Text
    phone_hours = ... # type: typing___Text
    expected_duration = ... # type: typing___Text
    purpose = ... # type: typing___Text
    topic = ... # type: typing___Text
    legal_disclaimer = ... # type: typing___Text
    anonymous = ... # type: builtin___bool

    def __init__(self,
        *,
        legal_entity : typing___Optional[typing___Text] = None,
        postal_address : typing___Optional[typing___Text] = None,
        email_address : typing___Optional[typing___Text] = None,
        phone_number : typing___Optional[typing___Text] = None,
        phone_hours : typing___Optional[typing___Text] = None,
        expected_duration : typing___Optional[typing___Text] = None,
        purpose : typing___Optional[typing___Text] = None,
        topic : typing___Optional[typing___Text] = None,
        legal_disclaimer : typing___Optional[typing___Text] = None,
        anonymous : typing___Optional[builtin___bool] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> SurveyInfo: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> SurveyInfo: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"anonymous",b"anonymous",u"email_address",b"email_address",u"expected_duration",b"expected_duration",u"legal_disclaimer",b"legal_disclaimer",u"legal_entity",b"legal_entity",u"phone_hours",b"phone_hours",u"phone_number",b"phone_number",u"postal_address",b"postal_address",u"purpose",b"purpose",u"topic",b"topic"]) -> None: ...
global___SurveyInfo = SurveyInfo

class Question(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def open_question(self) -> global___OpenQuestion: ...

    @property
    def single_choice_question(self) -> global___SingleChoiceQuestion: ...

    @property
    def multiple_choice_question(self) -> global___MultipleChoiceQuestion: ...

    @property
    def scale_question(self) -> global___ScaleQuestion: ...

    @property
    def single_parameter_question(self) -> global___SingleParameterQuestion: ...

    @property
    def multiple_parameter_question(self) -> global___MultipleParameterQuestion: ...

    def __init__(self,
        *,
        open_question : typing___Optional[global___OpenQuestion] = None,
        single_choice_question : typing___Optional[global___SingleChoiceQuestion] = None,
        multiple_choice_question : typing___Optional[global___MultipleChoiceQuestion] = None,
        scale_question : typing___Optional[global___ScaleQuestion] = None,
        single_parameter_question : typing___Optional[global___SingleParameterQuestion] = None,
        multiple_parameter_question : typing___Optional[global___MultipleParameterQuestion] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> Question: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> Question: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"multiple_choice_question",b"multiple_choice_question",u"multiple_parameter_question",b"multiple_parameter_question",u"open_question",b"open_question",u"question",b"question",u"scale_question",b"scale_question",u"single_choice_question",b"single_choice_question",u"single_parameter_question",b"single_parameter_question"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"multiple_choice_question",b"multiple_choice_question",u"multiple_parameter_question",b"multiple_parameter_question",u"open_question",b"open_question",u"question",b"question",u"scale_question",b"scale_question",u"single_choice_question",b"single_choice_question",u"single_parameter_question",b"single_parameter_question"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions___Literal[u"question",b"question"]) -> typing_extensions___Literal["open_question","single_choice_question","multiple_choice_question","scale_question","single_parameter_question","multiple_parameter_question"]: ...
global___Question = Question

class OpenQuestion(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    question_text = ... # type: typing___Text

    def __init__(self,
        *,
        question_text : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> OpenQuestion: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> OpenQuestion: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"question_text",b"question_text"]) -> None: ...
global___OpenQuestion = OpenQuestion

class SingleChoiceQuestion(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    question_text = ... # type: typing___Text

    @property
    def choices(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[global___Choice]: ...

    def __init__(self,
        *,
        question_text : typing___Optional[typing___Text] = None,
        choices : typing___Optional[typing___Iterable[global___Choice]] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> SingleChoiceQuestion: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> SingleChoiceQuestion: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"choices",b"choices",u"question_text",b"question_text"]) -> None: ...
global___SingleChoiceQuestion = SingleChoiceQuestion

class MultipleChoiceQuestion(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    question_text = ... # type: typing___Text

    @property
    def choices(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[global___Choice]: ...

    def __init__(self,
        *,
        question_text : typing___Optional[typing___Text] = None,
        choices : typing___Optional[typing___Iterable[global___Choice]] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> MultipleChoiceQuestion: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> MultipleChoiceQuestion: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"choices",b"choices",u"question_text",b"question_text"]) -> None: ...
global___MultipleChoiceQuestion = MultipleChoiceQuestion

class ScaleQuestion(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class ScaleValue(google___protobuf___message___Message):
        DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
        value = ... # type: builtin___int
        label = ... # type: typing___Text

        def __init__(self,
            *,
            value : typing___Optional[builtin___int] = None,
            label : typing___Optional[typing___Text] = None,
            ) -> None: ...
        if sys.version_info >= (3,):
            @classmethod
            def FromString(cls, s: builtin___bytes) -> ScaleQuestion.ScaleValue: ...
        else:
            @classmethod
            def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> ScaleQuestion.ScaleValue: ...
        def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
        def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"label",b"label",u"value",b"value"]) -> None: ...
    global___ScaleValue = ScaleValue

    question_text = ... # type: typing___Text

    @property
    def min_value(self) -> global___ScaleQuestion.ScaleValue: ...

    @property
    def max_value(self) -> global___ScaleQuestion.ScaleValue: ...

    def __init__(self,
        *,
        question_text : typing___Optional[typing___Text] = None,
        min_value : typing___Optional[global___ScaleQuestion.ScaleValue] = None,
        max_value : typing___Optional[global___ScaleQuestion.ScaleValue] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ScaleQuestion: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> ScaleQuestion: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"max_value",b"max_value",u"min_value",b"min_value"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"max_value",b"max_value",u"min_value",b"min_value",u"question_text",b"question_text"]) -> None: ...
global___ScaleQuestion = ScaleQuestion

class SingleParameterQuestion(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    question_text = ... # type: typing___Text
    parameter_type = ... # type: typing___Text

    def __init__(self,
        *,
        question_text : typing___Optional[typing___Text] = None,
        parameter_type : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> SingleParameterQuestion: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> SingleParameterQuestion: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"parameter_type",b"parameter_type",u"question_text",b"question_text"]) -> None: ...
global___SingleParameterQuestion = SingleParameterQuestion

class MultipleParameterQuestion(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    question_text = ... # type: typing___Text
    parameter_type = ... # type: typing___Text

    def __init__(self,
        *,
        question_text : typing___Optional[typing___Text] = None,
        parameter_type : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> MultipleParameterQuestion: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> MultipleParameterQuestion: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"parameter_type",b"parameter_type",u"question_text",b"question_text"]) -> None: ...
global___MultipleParameterQuestion = MultipleParameterQuestion

class Choice(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    synonyms = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]
    value = ... # type: typing___Text

    @property
    def follow_up_question(self) -> global___Question: ...

    def __init__(self,
        *,
        synonyms : typing___Optional[typing___Iterable[typing___Text]] = None,
        follow_up_question : typing___Optional[global___Question] = None,
        value : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> Choice: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> Choice: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"follow_up_question",b"follow_up_question"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"follow_up_question",b"follow_up_question",u"synonyms",b"synonyms",u"value",b"value"]) -> None: ...
global___Choice = Choice

class Answer(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class UserInfo(google___protobuf___message___Message):
        DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
        first_name = ... # type: typing___Text
        last_name = ... # type: typing___Text
        phone_number = ... # type: typing___Text
        session_id = ... # type: typing___Text

        def __init__(self,
            *,
            first_name : typing___Optional[typing___Text] = None,
            last_name : typing___Optional[typing___Text] = None,
            phone_number : typing___Optional[typing___Text] = None,
            session_id : typing___Optional[typing___Text] = None,
            ) -> None: ...
        if sys.version_info >= (3,):
            @classmethod
            def FromString(cls, s: builtin___bytes) -> Answer.UserInfo: ...
        else:
            @classmethod
            def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> Answer.UserInfo: ...
        def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
        def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"first_name",b"first_name",u"last_name",b"last_name",u"phone_number",b"phone_number",u"session_id",b"session_id"]) -> None: ...
    global___UserInfo = UserInfo

    question_nr = ... # type: builtin___int
    session_id = ... # type: typing___Text
    answer_text = ... # type: typing___Text
    answer_parameter = ... # type: typing___Text
    answer_parameter_original = ... # type: typing___Text
    anonymous = ... # type: builtin___bool

    @property
    def user_information(self) -> global___Answer.UserInfo: ...

    def __init__(self,
        *,
        question_nr : typing___Optional[builtin___int] = None,
        session_id : typing___Optional[typing___Text] = None,
        answer_text : typing___Optional[typing___Text] = None,
        answer_parameter : typing___Optional[typing___Text] = None,
        answer_parameter_original : typing___Optional[typing___Text] = None,
        anonymous : typing___Optional[builtin___bool] = None,
        user_information : typing___Optional[global___Answer.UserInfo] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> Answer: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> Answer: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"anonymous",b"anonymous",u"is_anonymous",b"is_anonymous",u"user_information",b"user_information"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"anonymous",b"anonymous",u"answer_parameter",b"answer_parameter",u"answer_parameter_original",b"answer_parameter_original",u"answer_text",b"answer_text",u"is_anonymous",b"is_anonymous",u"question_nr",b"question_nr",u"session_id",b"session_id",u"user_information",b"user_information"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions___Literal[u"is_anonymous",b"is_anonymous"]) -> typing_extensions___Literal["anonymous","user_information"]: ...
global___Answer = Answer

class CreateSurveyRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def survey(self) -> global___Survey: ...

    def __init__(self,
        *,
        survey : typing___Optional[global___Survey] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> CreateSurveyRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> CreateSurveyRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"survey",b"survey"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"survey",b"survey"]) -> None: ...
global___CreateSurveyRequest = CreateSurveyRequest

class GetSurveyRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    survey_id = ... # type: typing___Text

    def __init__(self,
        *,
        survey_id : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> GetSurveyRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> GetSurveyRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"survey_id",b"survey_id"]) -> None: ...
global___GetSurveyRequest = GetSurveyRequest

class UpdateSurveyRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def survey(self) -> global___Survey: ...

    @property
    def update_mask(self) -> google___protobuf___field_mask_pb2___FieldMask: ...

    def __init__(self,
        *,
        survey : typing___Optional[global___Survey] = None,
        update_mask : typing___Optional[google___protobuf___field_mask_pb2___FieldMask] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> UpdateSurveyRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> UpdateSurveyRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"survey",b"survey",u"update_mask",b"update_mask"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"survey",b"survey",u"update_mask",b"update_mask"]) -> None: ...
global___UpdateSurveyRequest = UpdateSurveyRequest

class DeleteSurveyRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    survey_id = ... # type: typing___Text

    def __init__(self,
        *,
        survey_id : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> DeleteSurveyRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> DeleteSurveyRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"survey_id",b"survey_id"]) -> None: ...
global___DeleteSurveyRequest = DeleteSurveyRequest

class GetSurveyAnswersRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    session_id = ... # type: typing___Text

    def __init__(self,
        *,
        session_id : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> GetSurveyAnswersRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> GetSurveyAnswersRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"session_id",b"session_id"]) -> None: ...
global___GetSurveyAnswersRequest = GetSurveyAnswersRequest

class GetAllSurveyAnswersRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    survey_id = ... # type: typing___Text

    def __init__(self,
        *,
        survey_id : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> GetAllSurveyAnswersRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> GetAllSurveyAnswersRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"survey_id",b"survey_id"]) -> None: ...
global___GetAllSurveyAnswersRequest = GetAllSurveyAnswersRequest

class SurveyAnswersResponse(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    survey_id = ... # type: typing___Text

    @property
    def answers(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[global___Answer]: ...

    def __init__(self,
        *,
        survey_id : typing___Optional[typing___Text] = None,
        answers : typing___Optional[typing___Iterable[global___Answer]] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> SurveyAnswersResponse: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> SurveyAnswersResponse: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"answers",b"answers",u"survey_id",b"survey_id"]) -> None: ...
global___SurveyAnswersResponse = SurveyAnswersResponse

class ListSurveysRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    page_token = ... # type: typing___Text

    def __init__(self,
        *,
        page_token : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ListSurveysRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> ListSurveysRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"page_token",b"page_token"]) -> None: ...
global___ListSurveysRequest = ListSurveysRequest

class ListSurveysResponse(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    next_page_token = ... # type: typing___Text

    @property
    def surveys(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[global___Survey]: ...

    def __init__(self,
        *,
        surveys : typing___Optional[typing___Iterable[global___Survey]] = None,
        next_page_token : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ListSurveysResponse: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> ListSurveysResponse: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"next_page_token",b"next_page_token",u"surveys",b"surveys"]) -> None: ...
global___ListSurveysResponse = ListSurveysResponse

class AgentSurveyRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    survey_id = ... # type: typing___Text

    def __init__(self,
        *,
        survey_id : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> AgentSurveyRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> AgentSurveyRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"survey_id",b"survey_id"]) -> None: ...
global___AgentSurveyRequest = AgentSurveyRequest

class AgentSurveyResponse(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    parent = ... # type: typing___Text

    def __init__(self,
        *,
        parent : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> AgentSurveyResponse: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> AgentSurveyResponse: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"parent",b"parent"]) -> None: ...
global___AgentSurveyResponse = AgentSurveyResponse
