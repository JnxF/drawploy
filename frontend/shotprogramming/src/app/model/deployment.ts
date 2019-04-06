export interface Deployment {
  resources: Resource<DeploymentProperties>[];
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
