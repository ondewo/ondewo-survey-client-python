# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from ondewo.survey import fhir_pb2 as ondewo_dot_survey_dot_fhir__pb2
from ondewo.survey import survey_pb2 as ondewo_dot_survey_dot_survey__pb2

GRPC_GENERATED_VERSION = '1.67.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in ondewo/survey/fhir_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class FHIRStub(object):
    """///// FHIR Services ///////

    The following servicer was designed to support the FHIR standard.
    Both Questionnaires and Responses will be detected and transformed for a simpler usage.

    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateFHIRSurvey = channel.unary_unary(
                '/ondewo.survey.FHIR/CreateFHIRSurvey',
                request_serializer=ondewo_dot_survey_dot_fhir__pb2.CreateFHIRSurveyRequest.SerializeToString,
                response_deserializer=ondewo_dot_survey_dot_survey__pb2.Survey.FromString,
                _registered_method=True)
        self.GetFHIRSurveyAnswers = channel.unary_unary(
                '/ondewo.survey.FHIR/GetFHIRSurveyAnswers',
                request_serializer=ondewo_dot_survey_dot_survey__pb2.GetSurveyAnswersRequest.SerializeToString,
                response_deserializer=ondewo_dot_survey_dot_fhir__pb2.SurveyFHIRAnswersResponse.FromString,
                _registered_method=True)
        self.GetAllFHIRSurveyAnswers = channel.unary_unary(
                '/ondewo.survey.FHIR/GetAllFHIRSurveyAnswers',
                request_serializer=ondewo_dot_survey_dot_survey__pb2.GetAllSurveyAnswersRequest.SerializeToString,
                response_deserializer=ondewo_dot_survey_dot_fhir__pb2.SurveyFHIRAnswersResponse.FromString,
                _registered_method=True)


class FHIRServicer(object):
    """///// FHIR Services ///////

    The following servicer was designed to support the FHIR standard.
    Both Questionnaires and Responses will be detected and transformed for a simpler usage.

    """

    def CreateFHIRSurvey(self, request, context):
        """Create a Survey from FHIR format and an empty NLU Agent for it
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFHIRSurveyAnswers(self, request, context):
        """Get Survey Answers on FHIR format
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllFHIRSurveyAnswers(self, request, context):
        """Get all Survey Answers on FHIR format
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FHIRServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateFHIRSurvey': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateFHIRSurvey,
                    request_deserializer=ondewo_dot_survey_dot_fhir__pb2.CreateFHIRSurveyRequest.FromString,
                    response_serializer=ondewo_dot_survey_dot_survey__pb2.Survey.SerializeToString,
            ),
            'GetFHIRSurveyAnswers': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFHIRSurveyAnswers,
                    request_deserializer=ondewo_dot_survey_dot_survey__pb2.GetSurveyAnswersRequest.FromString,
                    response_serializer=ondewo_dot_survey_dot_fhir__pb2.SurveyFHIRAnswersResponse.SerializeToString,
            ),
            'GetAllFHIRSurveyAnswers': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllFHIRSurveyAnswers,
                    request_deserializer=ondewo_dot_survey_dot_survey__pb2.GetAllSurveyAnswersRequest.FromString,
                    response_serializer=ondewo_dot_survey_dot_fhir__pb2.SurveyFHIRAnswersResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ondewo.survey.FHIR', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('ondewo.survey.FHIR', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class FHIR(object):
    """///// FHIR Services ///////

    The following servicer was designed to support the FHIR standard.
    Both Questionnaires and Responses will be detected and transformed for a simpler usage.

    """

    @staticmethod
    def CreateFHIRSurvey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ondewo.survey.FHIR/CreateFHIRSurvey',
            ondewo_dot_survey_dot_fhir__pb2.CreateFHIRSurveyRequest.SerializeToString,
            ondewo_dot_survey_dot_survey__pb2.Survey.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetFHIRSurveyAnswers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ondewo.survey.FHIR/GetFHIRSurveyAnswers',
            ondewo_dot_survey_dot_survey__pb2.GetSurveyAnswersRequest.SerializeToString,
            ondewo_dot_survey_dot_fhir__pb2.SurveyFHIRAnswersResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetAllFHIRSurveyAnswers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ondewo.survey.FHIR/GetAllFHIRSurveyAnswers',
            ondewo_dot_survey_dot_survey__pb2.GetAllSurveyAnswersRequest.SerializeToString,
            ondewo_dot_survey_dot_fhir__pb2.SurveyFHIRAnswersResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
