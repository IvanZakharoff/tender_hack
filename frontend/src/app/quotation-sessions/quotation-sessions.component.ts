import { Component, ElementRef, ViewChild } from '@angular/core';
import { FormArray, FormControl, FormGroup, UntypedFormArray, UntypedFormBuilder, UntypedFormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { FileUploadService } from '../upload-service';
import { BehaviorSubject, finalize } from 'rxjs';

interface Session {
  URL: string;
  rules: number[];
}

interface SessionFiles {
  URL: string;
  tzFile: File;
  contractFile: File;
}

@Component({
  selector: 'app-quotation-sessions',
  templateUrl: './quotation-sessions.component.html',
  styleUrl: './quotation-sessions.component.css'
})

export class QuotationSessionsComponent {


  formGroup?: UntypedFormGroup;

  result?: any[];

  selectedRules: number[] = [];

  @ViewChild('openFileDialog') private openFileDialog!: ElementRef;
  @ViewChild('loadFileElement') private loadFileElement!: ElementRef;
  loading: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);

  constructor(
    private formBuilder: UntypedFormBuilder,
    private uploadService: FileUploadService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.buildForm();
    this.add();
  }

  get sessions(): UntypedFormArray {
    return this.formGroup?.controls['sessions'] as FormArray;
  }

  buildForm() {

    this.formGroup = this.formBuilder.group({
      sessions: this.formBuilder.array([]),
    });
  }

  add() {
    this.sessions?.push((this.formBuilder.group({
      URL: new FormControl(''),
      tzFile: new FormControl(''),
      contractFile: new FormControl(''),
      rules: new FormControl('')
    })));
  }

  delete(index: number) {
    this.sessions.removeAt(index);
  }

  selectFile(event: any, session: any, type: string): void {
    if (type == 'tz') {
      session.controls['tzFile'].value = Array.from(event.target?.files)[0];
    } else {
      session.controls['contractFile'].value = Array.from(event.target?.files)[0];
    }
  }

  changeRules(event: any, session: any): void {
    session.controls['rules'].value = event;
  }

  sendForChecking() {
    let sessionsData: Session[] = [];
    let filesData: SessionFiles[] = [];
    (this.sessions?.controls as FormGroup[]).forEach(item => {
      const session: Session = {
        URL: item.controls['URL'].value,
        rules: item.controls['rules'].value,
      }

      const sessionFiles: SessionFiles = {
        URL: item.controls['URL'].value,
        tzFile: item.controls['tzFile'].value,
        contractFile: item.controls['contractFile'].value,
      }

      sessionsData.push(session);
      filesData.push(sessionFiles);
    });
    this.uploadService.uploadData(sessionsData, filesData).pipe(
      finalize(() => this.loading.next(false))
    ).subscribe(data => {
      this.result = data
      this.router.navigate(['/checking-result'], { state: { data } });
    }
    )
  }

  getFileName(session: any, type: string): string {
    if (type == 'tz') {
      return session.controls['tzFile']?.value?.name;
    } else {
      return session.controls['contractFile']?.value?.name;
    }

  }

  selectForAllSessions(rules: number[]) {
    this.selectedRules = rules;
  }

}
