@description('Existing Azure Spring Apps instance name.')
param name string

param cpu string
param memory string
param instances int
@description('Deployed image registry server')
param image_server string

@description('Deployed image without registry server')
param image_image string

param server string
param image string
@description('Deployed image registry server')
param registry_server_lZ2A string

@description('Deployed image without registry server')
param container_image_lZ2A string

param bar string

resource spring_resource 'Microsoft.AppPlatform/Spring@2022-12-01' existing = {
    name: name
}

resource apps_bigapp 'Microsoft.AppPlatform/Spring/Apps@2022-12-01'  = {
    name: 'bigapp'
    parent: spring_resource
    properties: {
      public : true
    }
}

resource deployments_bigapp 'Microsoft.AppPlatform/Spring/Apps/Deployments@2022-12-01'  = {
    name: 'bigapp'
    parent: apps_bigapp
    properties: {
      active : true
      deploymentSettings : {
        resourceRequests : {
          cpu : '1'
          memory : '1Gi'
        }
      }
      source : {
        type : 'Container'
        customContainer : {
          server : 'mcr.microsoft.com'
          containerImage : 'azurespringapps/samples/hello-world:0.0.1'
        }
      }
    }
    sku : {
      tier : 'Enterprise'
      name : 'E0'
      capacity : 1
    }
}

resource apps_smallapp 'Microsoft.AppPlatform/Spring/Apps@2022-12-01'  = {
    name: 'smallapp'
    parent: spring_resource
}

resource deployments_smallapp 'Microsoft.AppPlatform/Spring/Apps/Deployments@2022-12-01'  = {
    name: 'smallapp'
    parent: apps_smallapp
    properties: {
      active : true
      deploymentSettings : {
        resourceRequests : {
          cpu : '1'
          memory : '512Mi'
        }
        environmentVariables : {
          foo : 'bar'
          bas : 'baz'
        }
      }
      source : {
        type : 'BuildResult'
        buildResultId : '<default>'
      }
    }
    sku : {
      tier : 'Enterprise'
      name : 'E0'
      capacity : 1
    }
}

resource apps_notreadyforvariable 'Microsoft.AppPlatform/Spring/Apps@2022-12-01'  = {
    name: 'notreadyforvariable'
    parent: spring_resource
}

resource deployments_notreadyforvariable 'Microsoft.AppPlatform/Spring/Apps/Deployments@2022-12-01'  = {
    name: 'notreadyforvariable'
    parent: apps_notreadyforvariable
    properties: {
      active : true
      deploymentSettings : {
        resourceRequests : {
          cpu : cpu
          memory : memory
        }
        environmentVariables : {
          foo : bar
        }
      }
      source : {
        type : 'Container'
        customContainer : {
          server : image_server
          containerImage : image_image
        }
      }
    }
    sku : {
      tier : 'Enterprise'
      name : 'E0'
      capacity : instances
    }
}

resource apps_imageapp1 'Microsoft.AppPlatform/Spring/Apps@2022-12-01'  = {
    name: 'imageapp1'
    parent: spring_resource
    properties: {
      public : true
    }
}

resource deployments_imageapp1 'Microsoft.AppPlatform/Spring/Apps/Deployments@2022-12-01'  = {
    name: 'imageapp1'
    parent: apps_imageapp1
    properties: {
      active : true
      deploymentSettings : {
        resourceRequests : {
          cpu : '1'
          memory : '1Gi'
        }
      }
      source : {
        type : 'Container'
        customContainer : {
          server : server
          containerImage : image
        }
      }
    }
    sku : {
      tier : 'Enterprise'
      name : 'E0'
      capacity : 1
    }
}

resource apps_imageapp2 'Microsoft.AppPlatform/Spring/Apps@2022-12-01'  = {
    name: 'imageapp2'
    parent: spring_resource
    properties: {
      public : true
    }
}

resource deployments_imageapp2 'Microsoft.AppPlatform/Spring/Apps/Deployments@2022-12-01'  = {
    name: 'imageapp2'
    parent: apps_imageapp2
    properties: {
      active : true
      deploymentSettings : {
        resourceRequests : {
          cpu : '1'
          memory : '1Gi'
        }
      }
      source : {
        type : 'Container'
        customContainer : {
          server : registry_server_lZ2A
          containerImage : container_image_lZ2A
        }
      }
    }
    sku : {
      tier : 'Enterprise'
      name : 'E0'
      capacity : 1
    }
}
