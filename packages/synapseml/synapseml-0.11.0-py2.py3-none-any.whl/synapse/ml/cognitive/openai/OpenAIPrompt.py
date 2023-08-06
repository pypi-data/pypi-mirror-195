# Copyright (C) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in project root for information.


import sys
if sys.version >= '3':
    basestring = str

from pyspark import SparkContext, SQLContext
from pyspark.sql import DataFrame
from pyspark.ml.param.shared import *
from pyspark import keyword_only
from pyspark.ml.util import JavaMLReadable, JavaMLWritable
from synapse.ml.core.platform import running_on_synapse_internal
from synapse.ml.core.serialize.java_params_patch import *
from pyspark.ml.wrapper import JavaTransformer, JavaEstimator, JavaModel
from pyspark.ml.evaluation import JavaEvaluator
from pyspark.ml.common import inherit_doc
from synapse.ml.core.schema.Utils import *
from pyspark.ml.param import TypeConverters
from synapse.ml.core.schema.TypeConversionUtils import generateTypeConverter, complexTypeConverter


@inherit_doc
class OpenAIPrompt(ComplexParamsMixin, JavaMLReadable, JavaMLWritable, JavaTransformer):
    """
    Args:
        AADToken (object): AAD Token used for authentication
        apiVersion (object): version of the api
        concurrency (int): max number of concurrent calls
        concurrentTimeout (float): max number seconds to wait on futures if concurrency >= 1
        deploymentName (object): The name of the deployment
        errorCol (str): column to hold http errors
        maxTokens (object): The maximum number of tokens to generate. Has minimum of 0.
        model (object): The name of the model to use
        outputCol (str): The name of the output column
        postProcessing (str): Post processing options: csv, json, regex
        postProcessingOptions (dict): Options (default): delimiter=',', jsonSchema, regex, regexGroup=0
        promptTemplate (str): The prompt. supports string interpolation {col1}: {col2}.
        stop (object): A sequence which indicates the end of the current document.
        subscriptionKey (object): the API key to use
        temperature (object): What sampling temperature to use. Higher values means the model will take more risks. Try 0.9 for more creative applications, and 0 (argmax sampling) for ones with a well-defined answer. We generally recommend using this or `top_p` but not both. Minimum of 0 and maximum of 2 allowed.
        timeout (float): number of seconds to wait before closing the connection
        url (str): Url of the service
    """

    AADToken = Param(Params._dummy(), "AADToken", "ServiceParam: AAD Token used for authentication")
    
    apiVersion = Param(Params._dummy(), "apiVersion", "ServiceParam: version of the api")
    
    concurrency = Param(Params._dummy(), "concurrency", "max number of concurrent calls", typeConverter=TypeConverters.toInt)
    
    concurrentTimeout = Param(Params._dummy(), "concurrentTimeout", "max number seconds to wait on futures if concurrency >= 1", typeConverter=TypeConverters.toFloat)
    
    deploymentName = Param(Params._dummy(), "deploymentName", "ServiceParam: The name of the deployment")
    
    errorCol = Param(Params._dummy(), "errorCol", "column to hold http errors", typeConverter=TypeConverters.toString)
    
    maxTokens = Param(Params._dummy(), "maxTokens", "ServiceParam: The maximum number of tokens to generate. Has minimum of 0.")
    
    model = Param(Params._dummy(), "model", "ServiceParam: The name of the model to use")
    
    outputCol = Param(Params._dummy(), "outputCol", "The name of the output column", typeConverter=TypeConverters.toString)
    
    postProcessing = Param(Params._dummy(), "postProcessing", "Post processing options: csv, json, regex", typeConverter=TypeConverters.toString)
    
    postProcessingOptions = Param(Params._dummy(), "postProcessingOptions", "Options (default): delimiter=',', jsonSchema, regex, regexGroup=0")
    
    promptTemplate = Param(Params._dummy(), "promptTemplate", "The prompt. supports string interpolation {col1}: {col2}.", typeConverter=TypeConverters.toString)
    
    stop = Param(Params._dummy(), "stop", "ServiceParam: A sequence which indicates the end of the current document.")
    
    subscriptionKey = Param(Params._dummy(), "subscriptionKey", "ServiceParam: the API key to use")
    
    temperature = Param(Params._dummy(), "temperature", "ServiceParam: What sampling temperature to use. Higher values means the model will take more risks. Try 0.9 for more creative applications, and 0 (argmax sampling) for ones with a well-defined answer. We generally recommend using this or `top_p` but not both. Minimum of 0 and maximum of 2 allowed.")
    
    timeout = Param(Params._dummy(), "timeout", "number of seconds to wait before closing the connection", typeConverter=TypeConverters.toFloat)
    
    url = Param(Params._dummy(), "url", "Url of the service", typeConverter=TypeConverters.toString)

    
    @keyword_only
    def __init__(
        self,
        java_obj=None,
        AADToken=None,
        AADTokenCol=None,
        apiVersion=None,
        apiVersionCol=None,
        concurrency=1,
        concurrentTimeout=None,
        deploymentName=None,
        deploymentNameCol=None,
        errorCol="Error",
        maxTokens=None,
        maxTokensCol=None,
        model=None,
        modelCol=None,
        outputCol="out",
        postProcessing="",
        postProcessingOptions={},
        promptTemplate=None,
        stop=None,
        stopCol=None,
        subscriptionKey=None,
        subscriptionKeyCol=None,
        temperature=None,
        temperatureCol=None,
        timeout=60.0,
        url=None
        ):
        super(OpenAIPrompt, self).__init__()
        if java_obj is None:
            self._java_obj = self._new_java_obj("com.microsoft.azure.synapse.ml.cognitive.openai.OpenAIPrompt", self.uid)
        else:
            self._java_obj = java_obj
        self._setDefault(concurrency=1)
        self._setDefault(errorCol="Error")
        self._setDefault(outputCol="out")
        self._setDefault(postProcessing="")
        self._setDefault(postProcessingOptions={})
        self._setDefault(timeout=60.0)
        if hasattr(self, "_input_kwargs"):
            kwargs = self._input_kwargs
        else:
            kwargs = self.__init__._input_kwargs
    
        if java_obj is None:
            for k,v in kwargs.items():
                if v is not None:
                    getattr(self, "set" + k[0].upper() + k[1:])(v)

    @keyword_only
    def setParams(
        self,
        AADToken=None,
        AADTokenCol=None,
        apiVersion=None,
        apiVersionCol=None,
        concurrency=1,
        concurrentTimeout=None,
        deploymentName=None,
        deploymentNameCol=None,
        errorCol="Error",
        maxTokens=None,
        maxTokensCol=None,
        model=None,
        modelCol=None,
        outputCol="out",
        postProcessing="",
        postProcessingOptions={},
        promptTemplate=None,
        stop=None,
        stopCol=None,
        subscriptionKey=None,
        subscriptionKeyCol=None,
        temperature=None,
        temperatureCol=None,
        timeout=60.0,
        url=None
        ):
        """
        Set the (keyword only) parameters
        """
        if hasattr(self, "_input_kwargs"):
            kwargs = self._input_kwargs
        else:
            kwargs = self.__init__._input_kwargs
        return self._set(**kwargs)

    @classmethod
    def read(cls):
        """ Returns an MLReader instance for this class. """
        return JavaMMLReader(cls)

    @staticmethod
    def getJavaPackage():
        """ Returns package name String. """
        return "com.microsoft.azure.synapse.ml.cognitive.openai.OpenAIPrompt"

    @staticmethod
    def _from_java(java_stage):
        module_name=OpenAIPrompt.__module__
        module_name=module_name.rsplit(".", 1)[0] + ".OpenAIPrompt"
        return from_java(java_stage, module_name)

    def setAADToken(self, value):
        """
        Args:
            AADToken: AAD Token used for authentication
        """
        if isinstance(value, list):
            value = SparkContext._active_spark_context._jvm.com.microsoft.azure.synapse.ml.param.ServiceParam.toSeq(value)
        self._java_obj = self._java_obj.setAADToken(value)
        return self
    
    def setAADTokenCol(self, value):
        """
        Args:
            AADToken: AAD Token used for authentication
        """
        self._java_obj = self._java_obj.setAADTokenCol(value)
        return self
    
    def setApiVersion(self, value):
        """
        Args:
            apiVersion: version of the api
        """
        if isinstance(value, list):
            value = SparkContext._active_spark_context._jvm.com.microsoft.azure.synapse.ml.param.ServiceParam.toSeq(value)
        self._java_obj = self._java_obj.setApiVersion(value)
        return self
    
    def setApiVersionCol(self, value):
        """
        Args:
            apiVersion: version of the api
        """
        self._java_obj = self._java_obj.setApiVersionCol(value)
        return self
    
    def setConcurrency(self, value):
        """
        Args:
            concurrency: max number of concurrent calls
        """
        self._set(concurrency=value)
        return self
    
    def setConcurrentTimeout(self, value):
        """
        Args:
            concurrentTimeout: max number seconds to wait on futures if concurrency >= 1
        """
        self._set(concurrentTimeout=value)
        return self
    
    def setDeploymentName(self, value):
        """
        Args:
            deploymentName: The name of the deployment
        """
        if isinstance(value, list):
            value = SparkContext._active_spark_context._jvm.com.microsoft.azure.synapse.ml.param.ServiceParam.toSeq(value)
        self._java_obj = self._java_obj.setDeploymentName(value)
        return self
    
    def setDeploymentNameCol(self, value):
        """
        Args:
            deploymentName: The name of the deployment
        """
        self._java_obj = self._java_obj.setDeploymentNameCol(value)
        return self
    
    def setErrorCol(self, value):
        """
        Args:
            errorCol: column to hold http errors
        """
        self._set(errorCol=value)
        return self
    
    def setMaxTokens(self, value):
        """
        Args:
            maxTokens: The maximum number of tokens to generate. Has minimum of 0.
        """
        if isinstance(value, list):
            value = SparkContext._active_spark_context._jvm.com.microsoft.azure.synapse.ml.param.ServiceParam.toSeq(value)
        self._java_obj = self._java_obj.setMaxTokens(value)
        return self
    
    def setMaxTokensCol(self, value):
        """
        Args:
            maxTokens: The maximum number of tokens to generate. Has minimum of 0.
        """
        self._java_obj = self._java_obj.setMaxTokensCol(value)
        return self
    
    def setModel(self, value):
        """
        Args:
            model: The name of the model to use
        """
        if isinstance(value, list):
            value = SparkContext._active_spark_context._jvm.com.microsoft.azure.synapse.ml.param.ServiceParam.toSeq(value)
        self._java_obj = self._java_obj.setModel(value)
        return self
    
    def setModelCol(self, value):
        """
        Args:
            model: The name of the model to use
        """
        self._java_obj = self._java_obj.setModelCol(value)
        return self
    
    def setOutputCol(self, value):
        """
        Args:
            outputCol: The name of the output column
        """
        self._set(outputCol=value)
        return self
    
    def setPostProcessing(self, value):
        """
        Args:
            postProcessing: Post processing options: csv, json, regex
        """
        self._set(postProcessing=value)
        return self
    
    def setPostProcessingOptions(self, value):
        """
        Args:
            postProcessingOptions: Options (default): delimiter=',', jsonSchema, regex, regexGroup=0
        """
        self._set(postProcessingOptions=value)
        return self
    
    def setPromptTemplate(self, value):
        """
        Args:
            promptTemplate: The prompt. supports string interpolation {col1}: {col2}.
        """
        self._set(promptTemplate=value)
        return self
    
    def setStop(self, value):
        """
        Args:
            stop: A sequence which indicates the end of the current document.
        """
        if isinstance(value, list):
            value = SparkContext._active_spark_context._jvm.com.microsoft.azure.synapse.ml.param.ServiceParam.toSeq(value)
        self._java_obj = self._java_obj.setStop(value)
        return self
    
    def setStopCol(self, value):
        """
        Args:
            stop: A sequence which indicates the end of the current document.
        """
        self._java_obj = self._java_obj.setStopCol(value)
        return self
    
    def setSubscriptionKey(self, value):
        """
        Args:
            subscriptionKey: the API key to use
        """
        if isinstance(value, list):
            value = SparkContext._active_spark_context._jvm.com.microsoft.azure.synapse.ml.param.ServiceParam.toSeq(value)
        self._java_obj = self._java_obj.setSubscriptionKey(value)
        return self
    
    def setSubscriptionKeyCol(self, value):
        """
        Args:
            subscriptionKey: the API key to use
        """
        self._java_obj = self._java_obj.setSubscriptionKeyCol(value)
        return self
    
    def setTemperature(self, value):
        """
        Args:
            temperature: What sampling temperature to use. Higher values means the model will take more risks. Try 0.9 for more creative applications, and 0 (argmax sampling) for ones with a well-defined answer. We generally recommend using this or `top_p` but not both. Minimum of 0 and maximum of 2 allowed.
        """
        if isinstance(value, list):
            value = SparkContext._active_spark_context._jvm.com.microsoft.azure.synapse.ml.param.ServiceParam.toSeq(value)
        self._java_obj = self._java_obj.setTemperature(value)
        return self
    
    def setTemperatureCol(self, value):
        """
        Args:
            temperature: What sampling temperature to use. Higher values means the model will take more risks. Try 0.9 for more creative applications, and 0 (argmax sampling) for ones with a well-defined answer. We generally recommend using this or `top_p` but not both. Minimum of 0 and maximum of 2 allowed.
        """
        self._java_obj = self._java_obj.setTemperatureCol(value)
        return self
    
    def setTimeout(self, value):
        """
        Args:
            timeout: number of seconds to wait before closing the connection
        """
        self._set(timeout=value)
        return self
    
    def setUrl(self, value):
        """
        Args:
            url: Url of the service
        """
        self._set(url=value)
        return self

    
    def getAADToken(self):
        """
        Returns:
            AADToken: AAD Token used for authentication
        """
        return self._java_obj.getAADToken()
    
    
    def getApiVersion(self):
        """
        Returns:
            apiVersion: version of the api
        """
        return self._java_obj.getApiVersion()
    
    
    def getConcurrency(self):
        """
        Returns:
            concurrency: max number of concurrent calls
        """
        return self.getOrDefault(self.concurrency)
    
    
    def getConcurrentTimeout(self):
        """
        Returns:
            concurrentTimeout: max number seconds to wait on futures if concurrency >= 1
        """
        return self.getOrDefault(self.concurrentTimeout)
    
    
    def getDeploymentName(self):
        """
        Returns:
            deploymentName: The name of the deployment
        """
        return self._java_obj.getDeploymentName()
    
    
    def getErrorCol(self):
        """
        Returns:
            errorCol: column to hold http errors
        """
        return self.getOrDefault(self.errorCol)
    
    
    def getMaxTokens(self):
        """
        Returns:
            maxTokens: The maximum number of tokens to generate. Has minimum of 0.
        """
        return self._java_obj.getMaxTokens()
    
    
    def getModel(self):
        """
        Returns:
            model: The name of the model to use
        """
        return self._java_obj.getModel()
    
    
    def getOutputCol(self):
        """
        Returns:
            outputCol: The name of the output column
        """
        return self.getOrDefault(self.outputCol)
    
    
    def getPostProcessing(self):
        """
        Returns:
            postProcessing: Post processing options: csv, json, regex
        """
        return self.getOrDefault(self.postProcessing)
    
    
    def getPostProcessingOptions(self):
        """
        Returns:
            postProcessingOptions: Options (default): delimiter=',', jsonSchema, regex, regexGroup=0
        """
        return self.getOrDefault(self.postProcessingOptions)
    
    
    def getPromptTemplate(self):
        """
        Returns:
            promptTemplate: The prompt. supports string interpolation {col1}: {col2}.
        """
        return self.getOrDefault(self.promptTemplate)
    
    
    def getStop(self):
        """
        Returns:
            stop: A sequence which indicates the end of the current document.
        """
        return self._java_obj.getStop()
    
    
    def getSubscriptionKey(self):
        """
        Returns:
            subscriptionKey: the API key to use
        """
        return self._java_obj.getSubscriptionKey()
    
    
    def getTemperature(self):
        """
        Returns:
            temperature: What sampling temperature to use. Higher values means the model will take more risks. Try 0.9 for more creative applications, and 0 (argmax sampling) for ones with a well-defined answer. We generally recommend using this or `top_p` but not both. Minimum of 0 and maximum of 2 allowed.
        """
        return self._java_obj.getTemperature()
    
    
    def getTimeout(self):
        """
        Returns:
            timeout: number of seconds to wait before closing the connection
        """
        return self.getOrDefault(self.timeout)
    
    
    def getUrl(self):
        """
        Returns:
            url: Url of the service
        """
        return self.getOrDefault(self.url)

    

    def setCustomServiceName(self, value):
        self._java_obj = self._java_obj.setCustomServiceName(value)
        return self
    
    def setEndpoint(self, value):
        self._java_obj = self._java_obj.setEndpoint(value)
        return self
    
    def _transform(self, dataset: DataFrame) -> DataFrame:
        if running_on_synapse_internal():
            from synapse.ml.mlflow import get_mlflow_env_config
            mlflow_env_configs = get_mlflow_env_config()
            self.setAADToken(mlflow_env_configs.driver_aad_token)
            self.setEndpoint(mlflow_env_configs.workload_endpoint + "/cognitive/api/")
        return super()._transform(dataset)
        