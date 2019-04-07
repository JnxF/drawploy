export interface Deployment {
  id: string;
  nameOperation: string;
  code: { resources: Resource<DeploymentProperties>[]; }
}

export interface DeploymentShort {
  name: string;
  id: string;
}

export interface Resource<T extends DeploymentProperties> {
  type: string;
  name: string;
  properties: T;
}

export interface DeploymentProperties {}

export interface ComputeV1Instance extends DeploymentProperties {
  zone: string;
}
