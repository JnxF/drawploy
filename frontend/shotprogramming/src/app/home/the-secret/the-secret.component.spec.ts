import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TheSecretComponent } from './the-secret.component';

describe('TheSecretComponent', () => {
  let component: TheSecretComponent;
  let fixture: ComponentFixture<TheSecretComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TheSecretComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TheSecretComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
