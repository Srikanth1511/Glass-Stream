@ECHO OFF
set DIRNAME=%~dp0
set APP_BASE_NAME=%~n0
set CLASSPATH=%DIRNAME%\gradle\wrapper\gradle-wrapper.jar
set JAVA_EXE=java
"%JAVA_EXE%" -Xmx64m -cp "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*
