export interface Deployment<T extends DeploymentProperties> {
  type: string;
  name: string;
  properties: T;
}

export interface DeploymentProperties {}

export interface ComputeV1InstanceProps extends DeploymentProperties {

}
