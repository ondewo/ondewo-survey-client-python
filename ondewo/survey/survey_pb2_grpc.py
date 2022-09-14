# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from ondewo.survey import survey_pb2 as ondewo_dot_survey_dot_survey__pb2


class SurveysStub(object):
    """///// Services ///////

    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateSurvey = channel.unary_unary(
                '/ondewo.survey.Surveys/CreateSurvey',
                request_serializer=ondewo_dot_survey_dot_survey__pb2.CreateSurveyRequest.SerializeToString,
                response_deserializer=ondewo_dot_survey_dot_survey__pb2.Survey.FromString,
                )
        self.GetSurvey = channel.unary_unary(
                '/ondewo.survey.Surveys/GetSurvey',
                request_serializer=ondewo_dot_survey_dot_survey__pb2.GetSurveyRequest.SerializeToString,
                response_deserializer=ondewo_dot_survey_dot_survey__pb2.Survey.FromString,
                )
        self.UpdateSurvey = channel.unary_unary(
                '/ondewo.survey.Surveys/UpdateSurvey',
                request_serializer=ondewo_dot_survey_dot_survey__pb2.UpdateSurveyRequest.SerializeToString,
                response_deserializer=ondewo_dot_survey_dot_survey__pb2.Survey.FromString,
                )
        self.DeleteSurvey = channel.unary_unary(
                '/ondewo.survey.Surveys/DeleteSurvey',
                request_serializer=ondewo_dot_survey_dot_survey__pb2.DeleteSurveyRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.ListSurveys = channel.unary_unary(
                '/ondewo.survey.Surveys/ListSurveys',
                request_serializer=ondewo_dot_survey_dot_survey__pb2.ListSurveysRequest.SerializeToString,
                response_deserializer=ondewo_dot_survey_dot_survey__pb2.ListSurveysResponse.FromString,
                )
        self.GetSurveyAnswers = channel.unary_unary(
                '/ondewo.survey.Surveys/GetSurveyAnswers',
                request_serializer=ondewo_dot_survey_dot_survey__pb2.GetSurveyAnswersRequest.SerializeToString,
                response_deserializer=ondewo_dot_survey_dot_survey__pb2.SurveyAnswersResponse.FromString,
                )
        self.GetAllSurveyAnswers = channel.unary_unary(
                '/ondewo.survey.Surveys/GetAllSurveyAnswers',
                request_serializer=ondewo_dot_survey_dot_survey__pb2.GetAllSurveyAnswersRequest.SerializeToString,
                response_deserializer=ondewo_dot_survey_dot_survey__pb2.SurveyAnswersResponse.FromString,
                )
        self.CreateAgentSurvey = channel.unary_unary(
                '/ondewo.survey.Surveys/CreateAgentSurvey',
                request_serializer=ondewo_dot_survey_dot_survey__pb2.AgentSurveyRequest.SerializeToString,
                response_deserializer=ondewo_dot_survey_dot_survey__pb2.AgentSurveyResponse.FromString,
                )
        self.UpdateAgentSurvey = channel.unary_unary(
                '/ondewo.survey.Surveys/UpdateAgentSurvey',
                request_serializer=ondewo_dot_survey_dot_survey__pb2.AgentSurveyRequest.SerializeToString,
                response_deserializer=ondewo_dot_survey_dot_survey__pb2.AgentSurveyResponse.FromString,
                )
        self.DeleteAgentSurvey = channel.unary_unary(
                '/ondewo.survey.Surveys/DeleteAgentSurvey',
                request_serializer=ondewo_dot_survey_dot_survey__pb2.AgentSurveyRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class SurveysServicer(object):
    """///// Services ///////

    """

    def CreateSurvey(self, request, context):
        """Create a Survey and an empty NLU Agent for it
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSurvey(self, request, context):
        """Retrieve a Survey message from the Database and return it
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateSurvey(self, request, context):
        """Update an existing Survey message from the Database and return it
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteSurvey(self, request, context):
        """Delete a survey and its associated agent (if existent)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListSurveys(self, request, context):
        """Returns the list of all surveys in the server
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSurveyAnswers(self, request, context):
        """Retrieve answers to survey questions collected in interactions with a survey agent for a specific session
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllSurveyAnswers(self, request, context):
        """Retrieve all answers to survey questions collected in interactions with a survey agent in any session
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateAgentSurvey(self, request, context):
        """Populate and configures an NLU Agent from a Survey
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateAgentSurvey(self, request, context):
        """Update an NLU agent from a survey
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteAgentSurvey(self, request, context):
        """Deletes all data of an NLU agent associated to a survey
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SurveysServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateSurvey': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateSurvey,
                    request_deserializer=ondewo_dot_survey_dot_survey__pb2.CreateSurveyRequest.FromString,
                    response_serializer=ondewo_dot_survey_dot_survey__pb2.Survey.SerializeToString,
            ),
            'GetSurvey': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSurvey,
                    request_deserializer=ondewo_dot_survey_dot_survey__pb2.GetSurveyRequest.FromString,
                    response_serializer=ondewo_dot_survey_dot_survey__pb2.Survey.SerializeToString,
            ),
            'UpdateSurvey': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateSurvey,
                    request_deserializer=ondewo_dot_survey_dot_survey__pb2.UpdateSurveyRequest.FromString,
                    response_serializer=ondewo_dot_survey_dot_survey__pb2.Survey.SerializeToString,
            ),
            'DeleteSurvey': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteSurvey,
                    request_deserializer=ondewo_dot_survey_dot_survey__pb2.DeleteSurveyRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'ListSurveys': grpc.unary_unary_rpc_method_handler(
                    servicer.ListSurveys,
                    request_deserializer=ondewo_dot_survey_dot_survey__pb2.ListSurveysRequest.FromString,
                    response_serializer=ondewo_dot_survey_dot_survey__pb2.ListSurveysResponse.SerializeToString,
            ),
            'GetSurveyAnswers': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSurveyAnswers,
                    request_deserializer=ondewo_dot_survey_dot_survey__pb2.GetSurveyAnswersRequest.FromString,
                    response_serializer=ondewo_dot_survey_dot_survey__pb2.SurveyAnswersResponse.SerializeToString,
            ),
            'GetAllSurveyAnswers': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllSurveyAnswers,
                    request_deserializer=ondewo_dot_survey_dot_survey__pb2.GetAllSurveyAnswersRequest.FromString,
                    response_serializer=ondewo_dot_survey_dot_survey__pb2.SurveyAnswersResponse.SerializeToString,
            ),
            'CreateAgentSurvey': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateAgentSurvey,
                    request_deserializer=ondewo_dot_survey_dot_survey__pb2.AgentSurveyRequest.FromString,
                    response_serializer=ondewo_dot_survey_dot_survey__pb2.AgentSurveyResponse.SerializeToString,
            ),
            'UpdateAgentSurvey': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateAgentSurvey,
                    request_deserializer=ondewo_dot_survey_dot_survey__pb2.AgentSurveyRequest.FromString,
                    response_serializer=ondewo_dot_survey_dot_survey__pb2.AgentSurveyResponse.SerializeToString,
            ),
            'DeleteAgentSurvey': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteAgentSurvey,
                    request_deserializer=ondewo_dot_survey_dot_survey__pb2.AgentSurveyRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ondewo.survey.Surveys', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Surveys(object):
    """///// Services ///////

    """

    @staticmethod
    def CreateSurvey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.survey.Surveys/CreateSurvey',
            ondewo_dot_survey_dot_survey__pb2.CreateSurveyRequest.SerializeToString,
            ondewo_dot_survey_dot_survey__pb2.Survey.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSurvey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.survey.Surveys/GetSurvey',
            ondewo_dot_survey_dot_survey__pb2.GetSurveyRequest.SerializeToString,
            ondewo_dot_survey_dot_survey__pb2.Survey.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateSurvey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.survey.Surveys/UpdateSurvey',
            ondewo_dot_survey_dot_survey__pb2.UpdateSurveyRequest.SerializeToString,
            ondewo_dot_survey_dot_survey__pb2.Survey.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteSurvey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.survey.Surveys/DeleteSurvey',
            ondewo_dot_survey_dot_survey__pb2.DeleteSurveyRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListSurveys(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.survey.Surveys/ListSurveys',
            ondewo_dot_survey_dot_survey__pb2.ListSurveysRequest.SerializeToString,
            ondewo_dot_survey_dot_survey__pb2.ListSurveysResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSurveyAnswers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.survey.Surveys/GetSurveyAnswers',
            ondewo_dot_survey_dot_survey__pb2.GetSurveyAnswersRequest.SerializeToString,
            ondewo_dot_survey_dot_survey__pb2.SurveyAnswersResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAllSurveyAnswers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.survey.Surveys/GetAllSurveyAnswers',
            ondewo_dot_survey_dot_survey__pb2.GetAllSurveyAnswersRequest.SerializeToString,
            ondewo_dot_survey_dot_survey__pb2.SurveyAnswersResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateAgentSurvey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.survey.Surveys/CreateAgentSurvey',
            ondewo_dot_survey_dot_survey__pb2.AgentSurveyRequest.SerializeToString,
            ondewo_dot_survey_dot_survey__pb2.AgentSurveyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateAgentSurvey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.survey.Surveys/UpdateAgentSurvey',
            ondewo_dot_survey_dot_survey__pb2.AgentSurveyRequest.SerializeToString,
            ondewo_dot_survey_dot_survey__pb2.AgentSurveyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteAgentSurvey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.survey.Surveys/DeleteAgentSurvey',
            ondewo_dot_survey_dot_survey__pb2.AgentSurveyRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
