---
name: caravaggio-ui
description: Implement Flutter presentation UI with CaravaggioUI components and CustomScaffold. Use when creating pages, forms, lists, dialogs, or any presentation layer UI in this project.
---

# CaravaggioUI — presentation patterns

Implement UI using `caravaggio_ui` **1.0.6** and project wrappers.

## Prerequisites

Read `docs/architecture/CARAVAGGIO_COMPONENTS.md` (full component catalog).

Policy and locations: `docs/architecture/WIDGETS_AND_CARAVAGGIO.md`.

```dart
import 'package:caravaggio_ui/caravaggio_ui.dart';
import 'package:<project>/widgets/common/custom_scaffold.dart';
```

---

## Pattern 1 — Page with scrollable content

Use `CustomScaffold` + `bodyBuilder` for lists and scroll views.

```dart
class ItemsPage extends StatelessWidget {
  static const String routeName = '/items';

  const ItemsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return CustomScaffold(
      title: CText.title('Items', size: TextSize.small),
      showBackButton: true,
      action: IconButton(
        icon: const Icon(Icons.add),
        onPressed: () { /* navigate to create */ },
      ),
      bodyBuilder: (context, topPadding) {
        return BlocBuilder<ItemsBloc, ItemsState>(
          builder: (context, state) => switch (state) {
            Loading() => Padding(
              padding: EdgeInsets.only(top: topPadding),
              child: const LoadingWidget(),
            ),
            Loaded(:final items) => ListView.builder(
              padding: EdgeInsets.only(top: topPadding, left: 16, right: 16),
              itemCount: items.length,
              itemBuilder: (context, index) => CTile.simple(
                title: items[index].name,
                onTap: () { /* detail */ },
              ),
            ),
            _ => const SizedBox.shrink(),
          },
        );
      },
    );
  }
}
```

**Root pages** (Home, Splash, Login): `showBackButton: false`, no title if not needed.

---

## Pattern 2 — Form

Forms live inside a page shell or component — no scaffold in reusable form components.

```dart
CTextField.bordered(
  decoration: CFieldDecoration(label: 'Email'),
  onChanged: (value) => bloc.add(EmailChanged(value)),
),
const SizedBox(height: 16),
CButton.elevated(
  radius: AppRadius.s,
  onPressed: isSubmitting ? null : onSubmit,
  child: isSubmitting
      ? SizedBox(
          width: 20,
          height: 20,
          child: CCircularProgressIndicator.primary(),
        )
      : CText.label('Submit'),
),
```

Use `CDatePicker`, `CDropdown`, `CCheckbox`, `CRadioGroup` as needed — see catalog.

---

## Pattern 3 — List component (no scaffold)

Reusable BLoC components omit scaffold; parent page wraps with `CustomScaffold`.

```dart
class TaskListComponent extends StatelessWidget {
  const TaskListComponent({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<TaskListBloc, TaskListState>(
      builder: (context, state) => switch (state) {
        Loading() => const LoadingWidget(),
        Loaded(:final items) => ListView.builder(
          itemCount: items.length,
          itemBuilder: (context, index) => CTile.simple(
            title: items[index].title,
            trailing: IconButton(
              icon: const Icon(Icons.delete),
              onPressed: () => context.read<TaskListBloc>().add(
                TaskListEvent.deleteRequested(items[index].id),
              ),
            ),
          ),
        ),
        Error(:final message) => ErrorWidget(message: message),
        _ => const UnknownStateWidget(),
      },
    );
  }
}
```

---

## Checklist

- [ ] Page uses `CustomScaffold`, not Material `Scaffold`
- [ ] Caravaggio components from catalog, not raw Material equivalents
- [ ] Shared widgets reused from `lib/widgets/common/`
- [ ] Failures via `ErrorLocalizer`
- [ ] `flutter analyze` passes
