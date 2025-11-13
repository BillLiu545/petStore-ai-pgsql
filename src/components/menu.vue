

<template>
  <div class="min-h-screen bg-gray-100 flex flex-col">
    <!-- Header -->
    <header class="bg-white shadow-md p-4 flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-gray-800">My App</h1>
      <nav class="space-x-4">
        <a href="#" class="text-gray-600 hover:text-gray-800">Home</a>
        <a href="#" class="text-gray-600 hover:text-gray-800">About</a>
        <a href="#" class="text-gray-600 hover:text-gray-800">Contact</a>
      </nav>
    </header>

    <!-- Sidebar + Main -->
    <div class="flex flex-1">
      <!-- Sidebar -->
      <aside class="w-64 bg-white shadow-md p-4 hidden md:block">
        <ul class="space-y-2">
          <li>
            <a href="#" class="block p-2 rounded hover:bg-gray-200 text-gray-700">Dashboard</a>
          </li>
          <li>
            <a href="#" class="block p-2 rounded hover:bg-gray-200 text-gray-700">Settings</a>
          </li>
          <li>
            <a href="#" class="block p-2 rounded hover:bg-gray-200 text-gray-700">Profile</a>
          </li>
        </ul>
      </aside>

      <!-- Main Content -->
      <main class="flex-1 p-6">
        <slot />
      </main>
    </div>

    <!-- Footer -->
    <footer class="bg-white text-center text-gray-500 p-4 shadow-inner">
      &copy; 2025 My Company. All rights reserved.
    </footer>
  </div>
</template>

<script>
export default {
  name: 'BaseLayout',
};
</script>

<style scoped>
/* Add custom styles if needed */
</style>