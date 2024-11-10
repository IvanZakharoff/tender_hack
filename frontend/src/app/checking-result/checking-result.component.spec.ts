import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CheckingResultComponent } from './checking-result.component';

describe('CheckingResultComponent', () => {
  let component: CheckingResultComponent;
  let fixture: ComponentFixture<CheckingResultComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [CheckingResultComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CheckingResultComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
