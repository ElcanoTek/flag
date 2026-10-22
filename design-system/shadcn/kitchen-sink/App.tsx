import * as React from "react"
import {
  BellIcon,
  CalendarIcon,
  ChevronDownIcon,
  DownloadIcon,
  MoonIcon,
  PlusIcon,
  SettingsIcon,
  SunIcon,
  Trash2Icon,
  TriangleAlertIcon,
  CircleCheckIcon,
  InfoIcon,
} from "lucide-react"
import { toast } from "sonner"

import { useFlagTheme } from "@/hooks/use-flag-theme"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { Avatar, AvatarBadge, AvatarFallback, AvatarGroup, AvatarGroupCount } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
  CommandShortcut,
} from "@/components/ui/command"
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Popover,
  PopoverContent,
  PopoverDescription,
  PopoverHeader,
  PopoverTitle,
  PopoverTrigger,
} from "@/components/ui/popover"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet"
import { Skeleton } from "@/components/ui/skeleton"
import { Toaster } from "@/components/ui/sonner"
import { Switch } from "@/components/ui/switch"
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

function Section({ title, id, children }: { title: string; id: string; children: React.ReactNode }) {
  return (
    <section aria-labelledby={id} data-section={id} className="rounded-lg border bg-card p-6 shadow-(--shadow-section) max-sm:p-4">
      <h2 id={id} className="mb-4 font-heading text-subtitle font-bold">
        {title}
      </h2>
      <div className="flex flex-col gap-4">{children}</div>
    </section>
  )
}

function Row({ children }: { children: React.ReactNode }) {
  return <div className="flex flex-wrap items-center gap-3">{children}</div>
}

function ThemeToggle() {
  const theme = useFlagTheme()
  const dark = theme === "dark"
  return (
    <Button
      variant="secondary"
      size="icon"
      aria-pressed={dark}
      aria-label={dark ? "Switch to light mode" : "Switch to dark mode"}
      onClick={() => {
        const next = dark ? "light" : "dark"
        try {
          localStorage.setItem("flag-theme-preference", next)
        } catch {
          /* ignore */
        }
        document.documentElement.setAttribute("data-theme", next)
      }}
    >
      {dark ? <MoonIcon /> : <SunIcon />}
    </Button>
  )
}

const rows = [
  { id: "T-1023", name: "Daily Optimization", status: "success", runs: 1204 },
  { id: "T-1024", name: "Supply Audit", status: "running", runs: 87 },
  { id: "T-1025", name: "Weekly Forecast", status: "scheduled", runs: 52 },
  { id: "T-1026", name: "Deal Sync", status: "error", runs: 311 },
] as const

export function App() {
  const [notify, setNotify] = React.useState(true)
  return (
    <TooltipProvider>
      <div className="min-h-screen bg-(image:--gradient-bg-home-signature) text-foreground">
        <main className="mx-auto flex max-w-(--container-default) flex-col gap-6 p-6 max-sm:p-4">
          <header className="flex items-start justify-between gap-4">
            <div>
              <p className="text-overline tracking-widest text-muted-foreground uppercase">Elcano Internal</p>
              <h1 className="font-heading text-title font-bold">Flag shadcn/ui kitchen sink</h1>
              <p className="mt-1 max-w-3xl text-subtle">
                Every item in Flag's shadcn registry, installed with <code className="font-mono text-body-md">shadcn add @flag/…</code>.
              </p>
            </div>
            <ThemeToggle />
          </header>

          <Section title="Button" id="button">
            <Row>
              <Button>Primary</Button>
              <Button variant="secondary">Secondary</Button>
              <Button variant="outline">Outline</Button>
              <Button variant="ghost">Ghost</Button>
              <Button variant="destructive">Delete</Button>
              <Button variant="link">Link</Button>
              <Button disabled>Disabled</Button>
            </Row>
            <Row>
              <Button size="lg"><PlusIcon />New task</Button>
              <Button size="sm" variant="secondary"><DownloadIcon />Export</Button>
              <Button size="xs" variant="ghost">Extra small</Button>
              <Button size="icon" variant="secondary" aria-label="Settings"><SettingsIcon /></Button>
              <Button size="icon-sm" variant="ghost" aria-label="Notifications"><BellIcon /></Button>
              <Button size="icon-sm" variant="destructive" aria-label="Delete row"><Trash2Icon /></Button>
            </Row>
          </Section>

          <Section title="Input, Textarea, Label, Select" id="inputs">
            <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
              <div className="grid gap-2">
                <Label htmlFor="email">Email</Label>
                <Input id="email" type="email" placeholder="team@example.com" />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="search">Search</Label>
                <Input id="search" type="search" placeholder="Search tasks" />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="invalid">Campaign ID</Label>
                <Input id="invalid" aria-invalid="true" aria-describedby="invalid-help" defaultValue="CMP-??" />
                <p id="invalid-help" className="text-caption text-(--color-status-error-fg)">Use the form CMP-1234.</p>
              </div>
              <div className="grid gap-2">
                <Label htmlFor="disabled">Disabled</Label>
                <Input id="disabled" disabled placeholder="Not editable" />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="status-select">Status</Label>
                <Select defaultValue="running">
                  <SelectTrigger id="status-select" className="w-full" data-open="select">
                    <SelectValue placeholder="Pick a status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectGroup>
                      <SelectLabel>Lifecycle</SelectLabel>
                      <SelectItem value="pending">Pending</SelectItem>
                      <SelectItem value="scheduled">Scheduled</SelectItem>
                      <SelectItem value="running">Running</SelectItem>
                      <SelectItem value="success">Success</SelectItem>
                      <SelectItem value="cancelled" disabled>Cancelled</SelectItem>
                    </SelectGroup>
                  </SelectContent>
                </Select>
              </div>
              <div className="grid gap-2">
                <Label htmlFor="date">Start date</Label>
                <Input id="date" type="date" defaultValue="2026-10-22" />
              </div>
              <div className="grid gap-2 md:col-span-3">
                <Label htmlFor="notes">Notes</Label>
                <Textarea id="notes" placeholder="Anything the reviewer should know" />
              </div>
            </div>
          </Section>

          <Section title="Checkbox, Radio Group, Switch" id="choices">
            <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
              <div className="grid gap-3">
                <div className="flex items-center gap-2">
                  <Checkbox id="c1" checked={notify} onCheckedChange={(v) => setNotify(v === true)} />
                  <Label htmlFor="c1" className="text-body-md text-foreground">Notify on completion</Label>
                </div>
                <div className="flex items-center gap-2">
                  <Checkbox id="c2" />
                  <Label htmlFor="c2" className="text-body-md text-foreground">Archive results</Label>
                </div>
                <div className="flex items-center gap-2">
                  <Checkbox id="c3" disabled />
                  <Label htmlFor="c3" className="text-body-md text-foreground">Disabled</Label>
                </div>
              </div>
              <RadioGroup defaultValue="weekly" aria-label="Schedule">
                <div className="flex items-center gap-2">
                  <RadioGroupItem value="daily" id="r1" />
                  <Label htmlFor="r1" className="text-body-md text-foreground">Daily</Label>
                </div>
                <div className="flex items-center gap-2">
                  <RadioGroupItem value="weekly" id="r2" />
                  <Label htmlFor="r2" className="text-body-md text-foreground">Weekly</Label>
                </div>
                <div className="flex items-center gap-2">
                  <RadioGroupItem value="monthly" id="r3" disabled />
                  <Label htmlFor="r3" className="text-body-md text-foreground">Monthly (disabled)</Label>
                </div>
              </RadioGroup>
              <div className="grid gap-3">
                <div className="flex items-center gap-3">
                  <Switch id="s1" defaultChecked aria-label="Index Exchange" />
                  <Label htmlFor="s1" className="text-body-md text-foreground">Index Exchange</Label>
                </div>
                <div className="flex items-center gap-3">
                  <Switch id="s2" aria-label="Magnite" />
                  <Label htmlFor="s2" className="text-body-md text-foreground">Magnite</Label>
                </div>
                <div className="flex items-center gap-3">
                  <Switch id="s3" size="lg" defaultChecked aria-label="Large switch" />
                  <Label htmlFor="s3" className="text-body-md text-foreground">Large</Label>
                </div>
              </div>
            </div>
          </Section>

          <Section title="Card, Badge, Avatar, Separator" id="cards">
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              <Card>
                <CardHeader>
                  <CardTitle>Weekly forecast</CardTitle>
                  <CardDescription>Projected spend for the next seven days.</CardDescription>
                  <CardAction>
                    <Badge variant="scheduled">scheduled</Badge>
                  </CardAction>
                </CardHeader>
                <CardContent>
                  <p className="text-subtle">Runs every Monday at 06:00 UTC across 14 campaigns.</p>
                </CardContent>
                <CardFooter>
                  <Button size="sm">Run now</Button>
                  <Button size="sm" variant="ghost">Edit</Button>
                </CardFooter>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Status badges</CardTitle>
                  <CardDescription>The task status set, plus shadcn's variants.</CardDescription>
                </CardHeader>
                <CardContent className="flex flex-col gap-4">
                  <div className="flex flex-wrap gap-2">
                    {(["pending", "scheduled", "assigned", "leased", "running", "analyzing", "success", "warning", "error", "cancelled"] as const).map((s) => (
                      <Badge key={s} variant={s}>{s}</Badge>
                    ))}
                  </div>
                  <Separator />
                  <div className="flex flex-wrap gap-2">
                    <Badge>default</Badge>
                    <Badge variant="secondary">secondary</Badge>
                    <Badge variant="outline">outline</Badge>
                    <Badge variant="destructive">destructive</Badge>
                    <Badge variant="accent">accent</Badge>
                  </div>
                  <Separator />
                  <div className="flex items-center gap-4">
                    <Avatar size="sm"><AvatarFallback>BA</AvatarFallback></Avatar>
                    <Avatar><AvatarFallback>EL</AvatarFallback><AvatarBadge /></Avatar>
                    <Avatar size="lg"><AvatarFallback>FC</AvatarFallback></Avatar>
                    <AvatarGroup>
                      <Avatar><AvatarFallback>JD</AvatarFallback></Avatar>
                      <Avatar><AvatarFallback>MK</AvatarFallback></Avatar>
                      <AvatarGroupCount>+3</AvatarGroupCount>
                    </AvatarGroup>
                  </div>
                </CardContent>
              </Card>
            </div>
          </Section>

          <Section title="Alert, Skeleton" id="feedback">
            <Alert>
              <InfoIcon />
              <AlertTitle>Sync paused</AlertTitle>
              <AlertDescription>Deal sync resumes when the SSP token is renewed.</AlertDescription>
            </Alert>
            <Alert variant="success">
              <CircleCheckIcon />
              <AlertTitle>Report delivered</AlertTitle>
              <AlertDescription>Sent to 4 recipients at 09:12.</AlertDescription>
            </Alert>
            <Alert variant="warning">
              <TriangleAlertIcon />
              <AlertTitle>Budget at 92%</AlertTitle>
              <AlertDescription>Lower bids or extend the cap before Friday.</AlertDescription>
            </Alert>
            <Alert variant="destructive">
              <TriangleAlertIcon />
              <AlertTitle>Upload failed</AlertTitle>
              <AlertDescription>The file has no header row. Add one and upload again.</AlertDescription>
            </Alert>
            <div className="flex items-center gap-4" role="status" aria-busy="true">
              <span className="sr-only">Loading example</span>
              <Skeleton className="size-10 rounded-full" />
              <div className="grid flex-1 gap-2">
                <Skeleton className="h-4 w-2/3" />
                <Skeleton className="h-4 w-1/2" />
              </div>
            </div>
          </Section>

          <Section title="Tabs" id="tabs">
            <Tabs defaultValue="list">
              <TabsList aria-label="Calendar view">
                <TabsTrigger value="list">List</TabsTrigger>
                <TabsTrigger value="week">Week</TabsTrigger>
                <TabsTrigger value="month">Month</TabsTrigger>
              </TabsList>
              <TabsContent value="list" className="text-subtle">Segmented (default): the selected option sits on the primary fill.</TabsContent>
              <TabsContent value="week" className="text-subtle">Week view.</TabsContent>
              <TabsContent value="month" className="text-subtle">Month view.</TabsContent>
            </Tabs>
            <Tabs defaultValue="overview">
              <TabsList variant="line" aria-label="Task sections">
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="runs">Runs</TabsTrigger>
                <TabsTrigger value="settings">Settings</TabsTrigger>
                <TabsTrigger value="audit" disabled>Audit</TabsTrigger>
              </TabsList>
              <TabsContent value="overview" className="text-subtle">Line: page tabs with an accent underline.</TabsContent>
              <TabsContent value="runs" className="text-subtle">Runs.</TabsContent>
              <TabsContent value="settings" className="text-subtle">Settings.</TabsContent>
            </Tabs>
          </Section>

          <Section title="Table, Scroll Area" id="table">
            <Table>
              <TableCaption>Recent tasks</TableCaption>
              <TableHeader>
                <TableRow>
                  <TableHead>ID</TableHead>
                  <TableHead>Name</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead className="text-right">Runs</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {rows.map((r, i) => (
                  <TableRow key={r.id} interactive data-state={i === 1 ? "selected" : undefined}>
                    <TableCell className="font-mono text-caption">{r.id}</TableCell>
                    <TableCell>{r.name}</TableCell>
                    <TableCell><Badge variant={r.status}>{r.status}</Badge></TableCell>
                    <TableCell className="text-right">{r.runs.toLocaleString("en-US")}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
            <ScrollArea className="h-36 w-full max-w-sm rounded-md border" tabIndex={0} aria-label="Release notes">
              <div className="p-4">
                {Array.from({ length: 14 }, (_, i) => (
                  <p key={i} className="py-1 text-body-md text-subtle">v2.{14 - i}.0 — token and component updates</p>
                ))}
              </div>
            </ScrollArea>
          </Section>

          <Section title="Command" id="command">
            <Command className="max-w-md rounded-lg border border-(--color-selected-border) shadow-(--shadow-popover)" label="Command menu">
              <CommandInput placeholder="Search tools…" aria-label="Search tools" />
              <CommandList>
                <CommandEmpty>No tools match.</CommandEmpty>
                <CommandGroup heading="Connectors">
                  <CommandItem><CalendarIcon />Schedule a report<CommandShortcut>⌘S</CommandShortcut></CommandItem>
                  <CommandItem><DownloadIcon />Export deals</CommandItem>
                  <CommandItem disabled><BellIcon />Notifications (soon)</CommandItem>
                </CommandGroup>
                <CommandSeparator />
                <CommandGroup heading="Settings">
                  <CommandItem><SettingsIcon />Preferences</CommandItem>
                </CommandGroup>
              </CommandList>
            </Command>
          </Section>

          <Section title="Overlays: Dialog, Alert Dialog, Sheet, Dropdown Menu, Popover, Tooltip, Toast" id="overlays">
            <Row>
              <Dialog>
                <DialogTrigger asChild><Button variant="secondary" data-open="dialog">Open dialog</Button></DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Rename task</DialogTitle>
                    <DialogDescription>The new name shows in reports from the next run.</DialogDescription>
                  </DialogHeader>
                  <div className="grid gap-2">
                    <Label htmlFor="task-name">Name</Label>
                    <Input id="task-name" defaultValue="Weekly Forecast" />
                  </div>
                  <DialogFooter>
                    <DialogClose asChild><Button variant="secondary">Cancel</Button></DialogClose>
                    <Button>Save</Button>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
              <AlertDialog>
                <AlertDialogTrigger asChild><Button variant="destructive" data-open="alert-dialog">Delete task</Button></AlertDialogTrigger>
                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle>Delete “Weekly Forecast”?</AlertDialogTitle>
                    <AlertDialogDescription>Its 52 past runs are kept; future runs stop.</AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel>Cancel</AlertDialogCancel>
                    <AlertDialogAction variant="destructive">Delete</AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
              <Sheet>
                <SheetTrigger asChild><Button variant="outline" data-open="sheet">Open sheet</Button></SheetTrigger>
                <SheetContent>
                  <SheetHeader>
                    <SheetTitle>Task details</SheetTitle>
                    <SheetDescription>T-1025 · Weekly Forecast</SheetDescription>
                  </SheetHeader>
                  <div className="grid gap-2 px-6">
                    <Label htmlFor="sheet-owner">Owner</Label>
                    <Input id="sheet-owner" defaultValue="ads@example.com" />
                  </div>
                  <SheetFooter>
                    <Button>Save changes</Button>
                  </SheetFooter>
                </SheetContent>
              </Sheet>
              <DropdownMenu>
                <DropdownMenuTrigger asChild><Button variant="secondary" data-open="dropdown">Actions<ChevronDownIcon /></Button></DropdownMenuTrigger>
                <DropdownMenuContent className="w-56" align="start">
                  <DropdownMenuLabel>Task</DropdownMenuLabel>
                  <DropdownMenuItem><DownloadIcon />Export CSV<DropdownMenuShortcut>⌘E</DropdownMenuShortcut></DropdownMenuItem>
                  <DropdownMenuItem><SettingsIcon />Settings</DropdownMenuItem>
                  <DropdownMenuCheckboxItem checked>Show archived</DropdownMenuCheckboxItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem variant="destructive"><Trash2Icon />Delete</DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
              <Popover>
                <PopoverTrigger asChild><Button variant="secondary" data-open="popover">Filters</Button></PopoverTrigger>
                <PopoverContent align="start" aria-labelledby="filters-title">
                  <PopoverHeader>
                    <PopoverTitle id="filters-title">Filters</PopoverTitle>
                    <PopoverDescription>Narrow the task list.</PopoverDescription>
                  </PopoverHeader>
                  <div className="mt-3 flex items-center gap-2">
                    <Checkbox id="pf" defaultChecked />
                    <Label htmlFor="pf" className="text-body-md text-foreground">Only failed runs</Label>
                  </div>
                </PopoverContent>
              </Popover>
              <Tooltip>
                <TooltipTrigger asChild><Button size="icon" variant="ghost" aria-label="Download report" data-open="tooltip"><DownloadIcon /></Button></TooltipTrigger>
                <TooltipContent>Download report</TooltipContent>
              </Tooltip>
              <Button variant="secondary" data-open="toast" onClick={() => toast.success("Report delivered", { description: "Sent to 4 recipients." })}>Show toast</Button>
            </Row>
          </Section>
        </main>
        <Toaster position="bottom-right" />
      </div>
    </TooltipProvider>
  )
}
