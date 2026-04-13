import { TestBed } from '@angular/core/testing';

import { Solar } from './solar';

describe('Solar', () => {
  let service: Solar;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Solar);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
