from flask import Flask, Blueprint, request, jsonify, after_this_request
from flask import Response, make_response
from flask.json import JSONEncoder

from http import HTTPStatus

from logger import getLogger
from applicationSettings import ApplicationSettings
from cfClient import CfClient

class ExtendedApi:

    def __init__(self, appSettings: ApplicationSettings, cfClient: CfClient):
        self.appSettings = appSettings
        logger = getLogger(self.appSettings)
        self.logger = logger

        blueprint: Blueprint = Blueprint("BrokerApiExtentionBlueprint", "BrokerApiExtention", )
        self.blueprint = blueprint
        
        @blueprint.route("/v2/service_plans/<planId>/service_instances", methods=['GET'])
        def getServiceInstances(planId: str):
            page = request.args.get('page', default=1)
            pageSize= request.args.get('results-per-page', default=50)
            return cfClient.getServiceInstancesByPlanId(planId, page, pageSize)

        @blueprint.errorhandler(Exception)
        def error_handler(e):
            logger.exception(e)
            return {"error": type(e),"description": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    def getBlueprint(self) -> Blueprint:
        return self.blueprint