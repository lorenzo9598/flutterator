// const SizedBox(height: 8),
//                     CTextField.bordered(
//                       decoration: const CFieldDecoration(
//                         prefixIcon: Icon(Icons.email),
//                         labelText: 'Email',
//                       ),
//                       autocorrect: false,
//                       onChanged: (value) {
//                         context.read<SignInFormBloc>().add(SignInFormEvent.emailChanged(value));
//                       },
//                       validator: (_) {
//                         return context.read<SignInFormBloc>().state.emailAddress.value.fold(
//                               (f) => f.maybeMap(
//                                 invalidEmail: (_) => 'Invalid email',
//                                 orElse: () => null,
//                               ),
//                               (_) => null,
//                             );
//                       },
//                     ),
//                     const SizedBox(height: 8),
//                     CTextField.bordered(
//                       // controller: passwordController,
//                       decoration: const CFieldDecoration(
//                         prefixIcon: Icon(Icons.lock),
//                         labelText: 'Password',
//                       ),
//                       obscureText: true,
//                       autocorrect: false,
//                       onChanged: (value) {
//                         context.read<SignInFormBloc>().add(SignInFormEvent.passwordChanged(value));
//                       },
//                       validator: (_) {
//                         return context.read<SignInFormBloc>().state.password.value.fold(
//                               (f) => f.maybeMap(
//                                 shortPassword: (_) => 'Short password',
//                                 orElse: () => null,
//                               ),
//                               (_) => null,
//                             );
//                       },
//                     ),
//                     if (state.signInAction == SignInAction.signUp) ...[
//                       const SizedBox(height: 8),
//                       CTextField.bordered(
//                         decoration: const CFieldDecoration(
//                           prefixIcon: Icon(Icons.person),
//                           labelText: 'Confirm Password',
//                         ),
//                         obscureText: true,
//                         autocorrect: false,
//                         onChanged: (value) {
//                           context.read<SignInFormBloc>().add(SignInFormEvent.confirmPasswordChanged(value));
//                         },
//                         validator: (value) {
//                           return context.read<SignInFormBloc>().state.confirmPassword.value.fold(
//                                 (f) => f.maybeMap(
//                                   passwordsDoNotMatch: (_) => 'Passwords do not match',
//                                   orElse: () => null,
//                                 ),
//                                 (_) => null,
//                               );
//                         },
//                       ),
//                     ],
//                     const SizedBox(height: 8),
//                     CButton.elevated(
//                       radius: AppRadius.s,
//                       onPressed: () {
//                         if (state.signInAction == SignInAction.signIn) {
//                           context.read<SignInFormBloc>().add(const SignInFormEvent.signInWithEmailAndPasswordPressed());
//                         } else {
//                           context.read<SignInFormBloc>().add(const SignInFormEvent.registerWithEmailAndPasswordPressed());
//                         }
//                       },
//                       child: state.signInAction == SignInAction.signIn ? CText.label('SIGN IN') : CText.label('REGISTER'),
//                     ),
//                     const SizedBox(height: 16),
//                     Row(
//                       mainAxisAlignment: MainAxisAlignment.center,
//                       children: [
//                         CText.label(
//                           state.signInAction == SignInAction.signIn ? "Don't have an account? " : "Already have an account? ",
//                         ),
//                         GestureDetector(
//                           onTap: () {
//                             context.read<SignInFormBloc>().add(const SignInFormEvent.toggleSignInAction());
//                           },
//                           child: CText.label(
//                             state.signInAction == SignInAction.signIn ? 'Register' : 'Sign In',
//                           ).bold.withColor(Colors.blue),
//                         ),
//                       ],
//                     ),
