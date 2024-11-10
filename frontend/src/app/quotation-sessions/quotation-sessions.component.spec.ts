import { ComponentFixture, TestBed } from '@angular/core/testing';

import { QuotationSessionsComponent } from './quotation-sessions.component';

describe('QuotationSessionsComponent', () => {
  let component: QuotationSessionsComponent;
  let fixture: ComponentFixture<QuotationSessionsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [QuotationSessionsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(QuotationSessionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
