# 482 — Unit Tests for All shared/ui Components

**Priority:** P1  
**Repo:** signal-builder-frontend  
**Effort:** Medium (2-3 days)  
**Dependencies:** None

## Task Description
The shared/ui directory contains reusable components (Table, Dropdown, Select, ChipsInput, Popover, Edge, Icon, Checkbox) that are used throughout the app. Only Icon, Checkbox, and Popover have tests. The rest are untested, creating regression risk.

## Coding Prompt
```
Write React Testing Library tests for all untested components in 
/data/workspace/projects/signal-builder-frontend/src/shared/ui/

Components needing tests:
1. Table/Table.tsx — test renders with data, sorting, empty state
2. Dropdown/Dropdown.tsx — test opens/closes, selects option, keyboard nav
3. Select/Select.tsx — test renders options, handles onChange, disabled state
4. ChipsInput/ — test adding chip (Enter key), removing chip (X), max chips
5. Edge/Edge.tsx — test ReactFlow edge renders with correct style/label

For each component, create {ComponentName}/{ComponentName}.test.tsx:
- Import render, screen, userEvent from @testing-library
- Test: renders without crashing
- Test: renders with required props
- Test: interactive behavior (click, type, key events)
- Test: disabled state if applicable
- Test: error state if applicable

Example for Dropdown:
  it('opens dropdown on click', async () => {
    render(<Dropdown options={[{label:'A', value:'a'}]} onChange={jest.fn()} />)
    await userEvent.click(screen.getByRole('button'))
    expect(screen.getByText('A')).toBeInTheDocument()
  })

Run: yarn test --coverage
Target: >80% branch coverage on shared/ui/
```

## Acceptance Criteria
- [ ] All 5 missing test files created
- [ ] Each test file has minimum 4 test cases
- [ ] yarn test passes with no failures
- [ ] Coverage report shows >80% for shared/ui/
